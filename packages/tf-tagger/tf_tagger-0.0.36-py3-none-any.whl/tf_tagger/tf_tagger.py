# -*- coding: utf-8 -*-
import os
import pickle

import numpy as np
import pandas as pd
import tensorflow as tf
from bert import params_from_pretrained_ckpt
from tf_tagger.models.tagger_model import TaggerModel
from tf_tagger.utils.extract_entities import extract_entities
from tf_tagger.utils.label import Label
from tf_tagger.utils.tokenizer import Tokenizer
from tqdm import tqdm

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
            logical_gpus = tf.config.experimental.list_logical_devices('GPU')
            print('tf-tagger in GPU mode,', len(gpus), "Physical GPUs,",
                  len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
else:
    print('tf-tagger in CPU mode')


class TFTagger:
    def __init__(self,
                 embedding_size=100,
                 hidden_size=100,
                 bidirectional=True,
                 layer_size=1,
                 dropout=.5,
                 recurrent_dropout=.0,
                 embedding_weights=None,
                 embedding_trainable=True,
                 vocab_file=None,
                 bert=False,
                 bert_model_dir=None,
                 bert_max_length=4096,
                 bert_params=None,
                 bert_num_layers=None,
                 bert_trainable=False,
                 learning_rate=None,
                 optimizer='Adam',
                 loss='crf'):

        if bert:
            assert bert_params is not None or bert_model_dir is not None
            if bert_params is None:
                self.bert_params = params_from_pretrained_ckpt(bert_model_dir)
        else:
            self.bert_params = None

        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.bidirectional = bidirectional
        self.layer_size = layer_size
        self.dropout = dropout
        self.recurrent_dropout = recurrent_dropout
        self.model = None
        self.vocab_file = vocab_file
        self.bert = bert
        self.bert_model_dir = bert_model_dir
        self.bert_max_length = bert_max_length
        self.bert_num_layers = bert_num_layers
        self.bert_trainable = bert_trainable
        self.embedding_weights = embedding_weights
        self.embedding_trainable = embedding_trainable
        self.learning_rate = learning_rate
        self.optimizer = optimizer
        self.loss = loss

        self.tokenizer = None
        self.label = None
        self.batch_size = 32

    def build(self):
        model = TaggerModel(embedding_size=self.embedding_size,
                            hidden_size=self.hidden_size,
                            vocab_size=self.tokenizer.vocab_size,
                            tag_size=self.label.label_size,
                            dropout=self.dropout,
                            recurrent_dropout=self.recurrent_dropout,
                            embedding_weights=self.embedding_weights,
                            embedding_trainable=self.embedding_trainable,
                            layer_size=self.layer_size,
                            bidirectional=self.bidirectional,
                            bert=self.bert,
                            bert_model_dir=self.bert_model_dir,
                            bert_max_length=self.bert_max_length,
                            bert_params=self.bert_params,
                            bert_num_layers=self.bert_num_layers,
                            bert_trainable=self.bert_trainable,
                            loss=self.loss)
        model.build(tf.TensorShape([None, 4096]))
        model.summary()
        return model

    def fit(self,
            X,
            y,
            X_dev=None,
            y_dev=None,
            batch_size=None,
            epoch=100,
            save_best=None):
        """Model training."""

        if batch_size is None:
            batch_size = self.batch_size
        else:
            self.batch_size = batch_size

        if self.tokenizer is None:
            if self.vocab_file is not None:
                tokenizer = Tokenizer(self.vocab_file)
            else:
                tokenizer = Tokenizer()
                tokenizer.fit(X)
            self.tokenizer = tokenizer
        else:
            tokenizer = self.tokenizer

        if self.label is None:
            label = Label()
            label.fit(y)
            self.label = label
        else:
            label = self.label

        if self.model is None:
            model = self.build()
            self.model = model
        else:
            model = self.model

        if self.learning_rate is not None:
            if self.optimizer.lower() == 'sgd':
                optimizer = tf.keras.optimizers.SGD(self.learning_rate,
                                                    momentum=0.9)
            elif self.optimizer.lower() == 'nadam':
                optimizer = tf.keras.optimizers.Nadam(self.learning_rate)
            elif self.optimizer.lower() == 'rmsprop':
                optimizer = tf.keras.optimizers.RMSprop(self.learning_rate)
            else:
                optimizer = tf.keras.optimizers.Adam(self.learning_rate)
        else:
            if self.optimizer.lower() == 'sgd':
                optimizer = tf.keras.optimizers.SGD(momentum=0.9)
            elif self.optimizer.lower() == 'nadam':
                optimizer = tf.keras.optimizers.Nadam()
            elif self.optimizer.lower() == 'rmsprop':
                optimizer = tf.keras.optimizers.RMSprop()
            else:
                optimizer = tf.keras.optimizers.Adam()

        def gendata(X, y, batch_size):

            pos_lengths = [(i, len(x)) for i, x in enumerate(X)]
            pos_lengths = sorted(pos_lengths, key=lambda x: x[1], reverse=True)
            pos = [x[0] for x in pos_lengths]
            X = [X[i] for i in pos]
            y = [y[i] for i in pos]
            total_batch = int(np.ceil(len(X) / batch_size))
            points = list(range(total_batch))
            np.random.shuffle(points)

            for i in points:
                i_min = i * batch_size
                i_max = min((i + 1) * batch_size, len(X))
                x = tokenizer.transform(X[i_min:i_max])
                tags = label.transform(y[i_min:i_max])
                yield x, tags

        last_best = None
        for i_epoch in range(epoch):

            total_batch = int(np.ceil(len(X) / batch_size))
            pbar = tqdm(gendata(X, y, batch_size), total=total_batch, ncols=0)
            pbar.set_description(f'epoch: {i_epoch} loss: -')
            losses = []

            for x, tags in pbar:
                with tf.GradientTape() as tape:
                    loss = model.compute_loss(x, tags)
                    gradients = tape.gradient(loss, model.trainable_variables)
                    gradients = [
                        tf.clip_by_value(g, -5.0, 5.0) if g is not None else g
                        for g in gradients
                    ]
                    gradients = [
                        tf.clip_by_norm(g, 1.) if g is not None else g
                        for g in gradients
                    ]

                optimizer.apply_gradients(
                    zip(gradients, model.trainable_variables))
                loss = loss.numpy().sum()
                losses.append(loss)
                pbar.set_description(
                    f'epoch: {i_epoch} loss: {np.mean(losses):.4f}')
            if X_dev is not None and y_dev is not None:
                print('evaluate dev data')
                table = self.score_table(X_dev, y_dev, verbose=1)
                print(table)
                if save_best is not None:
                    f1 = table.iloc[-1]['f1score']
                    if last_best is None or f1 > last_best:
                        last_best = f1
                        print('save_best to:', save_best)
                        with open(save_best, 'wb') as fp:
                            pickle.dump(self, fp, protocol=4)
                    else:
                        print('save_best to: no better '
                              f'{f1:.4f} < {last_best:.4f}')

    def predict(self, X, verbose=False, batch_size=None):
        """Predict label."""
        assert self.model is not None, 'Intent not fit'
        batch_size = batch_size or self.batch_size

        pos_lengths = [(i, len(x)) for i, x in enumerate(X)]
        pos_lengths = sorted(pos_lengths, key=lambda x: x[1], reverse=True)
        pos = [x[0] for x in pos_lengths]
        X = [X[i] for i in pos]

        total_batch = int(np.ceil(len(X) / batch_size))
        pbar = range(total_batch)
        if verbose:
            pbar = tqdm(pbar, ncols=0)
        ret = []
        for i in pbar:
            i_min = i * batch_size
            i_max = min((i + 1) * batch_size, len(X))
            x = self.tokenizer.transform(X[i_min:i_max])
            x = self.model(x)
            x = x.numpy()
            ret += self.label.inverse_transform(x)
        for i in range(len(ret)):
            ret[i] = ret[i][1:1 + len(X[i])]
        ordered_ret = [None] * len(ret)
        for p, r in zip(pos, ret):
            ordered_ret[p] = r
        return ordered_ret

    def __getstate__(self):
        """Pickle compatible."""
        state = self.__dict__.copy()
        if self.model is not None:
            state['model_weights'] = state['model'].get_weights()
            del state['model']
        return state

    def __setstate__(self, state):
        """Pickle compatible."""
        if 'model_weights' in state:
            model_weights = state.get('model_weights')
            del state['model_weights']
            state['bert_model_dir'] = None
            self.__dict__.update(state)
            self.model = self.build()
            self.model.set_weights(model_weights)
        else:
            self.__dict__.update(state)

    def _get_sets(self, X, y, verbose, batch_size):
        preds = self.predict(X, verbose=verbose, batch_size=batch_size)
        pbar = enumerate(zip(preds, y))
        if verbose > 0:
            pbar = tqdm(pbar, total=len(y), ncols=0)

        apset = []
        arset = []
        for i, (pred, y_true) in pbar:
            pset = extract_entities(pred)
            rset = extract_entities(y_true)
            for item in pset:
                apset.append(tuple([i] + list(item)))
            for item in rset:
                arset.append(tuple([i] + list(item)))
        return apset, arset

    def score(self, X, y, batch_size=None, verbose=0, detail=False):
        """Calculate NER F1
        Based CONLL 2003 standard
        """
        apset, arset = self._get_sets(X, y, verbose, batch_size)
        pset = set(apset)
        rset = set(arset)
        inter = pset.intersection(rset)
        precision = len(inter) / len(pset) if pset else 1
        recall = len(inter) / len(rset) if rset else 1
        f1score = 0
        if precision + recall > 0:
            f1score = 2 * ((precision * recall) / (precision + recall))
        if detail:
            return precision, recall, f1score
        return f1score

    def score_table(self, X, y, batch_size=None, verbose=0):
        """Calculate NER F1
        Based CONLL 2003 standard
        """
        apset, arset = self._get_sets(X, y, verbose, batch_size)
        types = [x[3] for x in apset] + [x[3] for x in arset]
        types = sorted(set(types))
        rows = []
        for etype in types:
            pset = set([x for x in apset if x[3] == etype])
            rset = set([x for x in arset if x[3] == etype])
            inter = pset.intersection(rset)
            precision = len(inter) / len(pset) if pset else 1
            recall = len(inter) / len(rset) if rset else 1
            f1score = 0
            if precision + recall > 0:
                f1score = 2 * ((precision * recall) / (precision + recall))
            rows.append((etype, precision, recall, f1score))
        pset = set(apset)
        rset = set(arset)
        inter = pset.intersection(rset)
        precision = len(inter) / len(pset) if pset else 1
        recall = len(inter) / len(rset) if rset else 1
        f1score = 0
        if precision + recall > 0:
            f1score = 2 * ((precision * recall) / (precision + recall))
        rows.append(('TOTAL', precision, recall, f1score))
        df = pd.DataFrame(rows,
                          columns=['name', 'precision', 'recall', 'f1score'])
        df.index = df['name']
        df = df.drop('name', axis=1)
        return df
