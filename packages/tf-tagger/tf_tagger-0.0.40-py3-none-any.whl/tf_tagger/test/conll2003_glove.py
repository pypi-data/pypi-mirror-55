# -*- coding: utf-8 -*-
import os
import pickle
import numpy as np
from appdirs import user_cache_dir
from ..tf_tagger import TFTagger
from ..utils.text_reader import text_reader
from ..utils.read_vectors import read_vectors
from .get_conll2003 import main as get_conll2003


def test():
    
    cache_dir = user_cache_dir(appname='tf-tagger')

    train_path, dev_path, test_path = [
        os.path.join(cache_dir, x)
        for x in [
            'conll2003_eng_train.txt',
            'conll2003_eng_valid.txt',
            'conll2003_eng_test.txt'
        ]
    ]

    if not os.path.exists(train_path):
        get_conll2003()

    x_train, y_train = text_reader(train_path)
    x_dev, y_dev = text_reader(dev_path)
    x_test, y_test = text_reader(test_path)

    print('read_vectors start')
    words, embedding = read_vectors('./glove.840B.300d.txt', 300)
    print('read_vectors over')

    it = TFTagger(
        embedding_size=300,
        hidden_size=300,
        layer_size=1,
        dropout=0.5,
        vocab_file=words,
        embedding_weights=embedding,
        embedding_trainable=False
    )

    save_best = '/tmp/conll2003_glove.pkl'
    it.fit(x_train, y_train, x_dev, y_dev, batch_size=64, save_best=save_best, epoch=50)
    print(it.score_table(x_test, y_test))
    with open(save_best, 'rb') as fp:
        it = pickle.load(fp)
    print(it.score_table(x_test, y_test))


if __name__ == '__main__':
    test()
