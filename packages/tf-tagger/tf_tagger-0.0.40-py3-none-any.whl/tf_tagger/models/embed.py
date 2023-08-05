# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf


class Embed(tf.keras.Model):

    def __init__(self, embedding_size, vocab_size, weights, trainable):
        super(Embed, self).__init__(self)
        self.embedding_size = embedding_size
        self.vocab_size = vocab_size
        self.trainable = trainable

        with tf.device('/CPU:0'):
            if weights is not None:
                assert len(weights.shape) == 2
                assert weights.shape[0] == vocab_size, f'{weights.shape[0]} vs {vocab_size}'
                assert weights.shape[1] == embedding_size, f'{weights.shape[1]} vs {embedding_size}'
                weights = [tf.convert_to_tensor(weights, dtype=tf.float32)]
                self.emb = tf.keras.layers.Embedding(
                    vocab_size,
                    embedding_size,
                    weights=weights,
                    mask_zero=True
                )
            else:
                self.emb = tf.keras.layers.Embedding(
                    vocab_size,
                    embedding_size,
                    mask_zero=True
                )

    def call(self, inputs):
        x = inputs
        x = self.emb(x)
        return x

    def build(self, input_shape):
        self.emb.build(input_shape)
        self.built = True

    def compute_output_shape(self, input_shape):
        batch_size, lengths = input_shape
        return tf.TensorShape([batch_size, lengths, self.embedding_size])
