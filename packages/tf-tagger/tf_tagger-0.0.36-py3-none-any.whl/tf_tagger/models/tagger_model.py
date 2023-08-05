# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf

from .embed import Embed
from .encoder import Encoder
from .decoder import Decoder
from .encoder_bert import EncoderBert
from .decoder_softmax import DecoderSoftmax

class TaggerModel(tf.keras.Model):
    def __init__(self,
                 embedding_size,
                 hidden_size,
                 vocab_size,
                 tag_size,
                 dropout,
                 layer_size,
                 bidirectional,
                 embedding_weights,
                 embedding_trainable,
                 recurrent_dropout,
                 bert,
                 bert_model_dir,
                 bert_max_length,
                 bert_params,
                 bert_num_layers,
                 bert_trainable,
                 loss):
        super(TaggerModel, self).__init__(self)
        self.dropout = dropout
        self.bert = bert
        if bert:
            self.emb = EncoderBert(
                max_length=bert_max_length,
                model_dir=bert_model_dir,
                bert_params=bert_params,
                num_layers=bert_num_layers,
                trainable=bert_trainable
            )
        else:
            self.emb = Embed(
                embedding_size=embedding_size,
                vocab_size=vocab_size,
                weights=embedding_weights,
                trainable=embedding_trainable
            )
        self.en = Encoder(
            embedding_size=embedding_size,
            hidden_size=hidden_size,
            layer_size=layer_size,
            bidirectional=bidirectional,
            recurrent_dropout=recurrent_dropout
        )
        self.project = tf.keras.models.Sequential([
            tf.keras.layers.Dense(tag_size)
        ])
        if loss == 'crf':
            self.de = Decoder(tag_size=tag_size)
        elif loss == 'softmax':
            self.de = DecoderSoftmax(tag_size=tag_size)

    def build(self, input_shape):
        self.emb.build(input_shape)
        input_shape = self.emb.compute_output_shape(input_shape)
        self.en.build(input_shape)
        input_shape = self.en.compute_output_shape(input_shape)
        self.project.build(input_shape)
        input_shape = self.project.compute_output_shape(input_shape)
        self.de.build(input_shape)
        self.built = True

    def logits(self, inputs, training=False):
        lengths = tf.reduce_sum(tf.cast(tf.math.greater(inputs, 0), tf.int32), axis=-1)
        mask = tf.greater(inputs, 0)
        x = inputs
        x = self.emb(x)
        if training:
            x = tf.nn.dropout(x, rate=self.dropout)
        x = self.en(x)
        if training:
            x = tf.nn.dropout(x, rate=self.dropout)
        x = self.project(x)
        return x, lengths

    def call(self, inputs):
        logits, lengths = self.logits(inputs)
        return self.de(logits, lengths)

    def compute_loss(self, inputs, tags):
        logits, lengths = self.logits(inputs, training=True)
        return self.de.compute_loss(logits, lengths, tags)


if __name__ == "__main__":
    tm = TaggerModel(
        embedding_size=None,
        hidden_size=768,
        vocab_size=None,
        tag_size=10,
        dropout=.0,
        layer_size=None,
        bidirectional=None,
        bert=True,
        bert_model_dir='./chinese_L-12_H-768_A-12',
        bert_max_length=4096)
    from ..utils.tokenizer import Tokenizer
    tokenizer = Tokenizer('./chinese_L-12_H-768_A-12/vocab.txt')
    ids = tokenizer.transform([['我', '爱', '你']])
    r = tm(ids)
    print(r)