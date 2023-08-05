# -*- coding: utf-8 -*-
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

import numpy as np
import tensorflow as tf
from .crf import crf_decode, crf_log_likelihood


class Decoder(tf.keras.Model):

    def __init__(self, tag_size):
        super(Decoder, self).__init__(self)
        self.tag_size = tag_size
        initializer = tf.keras.initializers.GlorotUniform()
        self.transition_params = tf.Variable(
            initial_value=initializer(
                shape=(tag_size, tag_size),
                dtype=tf.dtypes.float32),
            name='crf/transition_params'
        )

    def call(self, inputs, lengths):
        """
        parameters:
            inputs [B, L, T]
            lengths [B]
        returns: [B, L]
        """
        tags_id, _ = crf_decode(
            inputs, self.transition_params, lengths)
        return tags_id

    def compute_loss(self, inputs, lengths, tags):
        """
        parameters:
            inputs [B, L, T]
            lengths [B]
            tags [B, L, N]
        returns: loss
        """
        sequence_log_likelihood, _ = crf_log_likelihood(
            inputs=inputs,
            tag_indices=tags,
            sequence_lengths=lengths,
            transition_params=self.transition_params)
        loss = tf.reduce_mean(-sequence_log_likelihood)
        return loss