# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf


class Encoder(tf.keras.Model):

    def __init__(self, embedding_size, hidden_size, layer_size, bidirectional, recurrent_dropout):
        self.embedding_size = embedding_size
        self.hidden_size = hidden_size
        self.layer_size = layer_size
        self.bidirectional = bidirectional
        self.recurrent_dropout = recurrent_dropout
        super(Encoder, self).__init__(self)

        self.lstm = []
        for _ in range(layer_size):
            if bidirectional:
                l = tf.keras.layers.Bidirectional(
                    tf.keras.layers.LSTM(
                        hidden_size, return_sequences=True,
                        recurrent_dropout=recurrent_dropout
                    )
                )
            else:
                l = tf.keras.layers.LSTM(hidden_size, return_sequences=True)
            self.lstm.append(l)

    def build(self, input_shape):
        for l in self.lstm:
            l.build(input_shape)
            input_shape = l.compute_output_shape(input_shape)
        self.built = True

    def call(self, inputs):
        x = inputs
        for l in self.lstm:
            x = l(x)
        return x

    def compute_output_shape(self, input_shape):
        batch_size, lengths, embedding_size = input_shape
        if self.bidirectional:
            return tf.TensorShape([batch_size, lengths, self.hidden_size * 2])
        return tf.TensorShape([batch_size, lengths, self.hidden_size])