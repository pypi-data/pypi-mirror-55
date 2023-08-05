# -*- coding: utf-8 -*-
import numpy as np
from .label import PAD, UNK, SOS, EOS

def read_vectors(vector_path,
                 dim=100):
    """Read vectors"""

    def random_vec():
        return np.random.uniform(
            -np.sqrt(3. / dim), np.sqrt(3. / dim), size=(1, dim))

    def zero_vec():
        return np.zeros((1, dim))

    words = [
        PAD,
        UNK,
        SOS,
        EOS
    ]
    vecs = [
        zero_vec(),
        random_vec(),
        random_vec(),
        random_vec()
    ]

    exists = {k: True for k in words}
    with open(vector_path, 'r') as fobj:
        lines = fobj.read().split('\n')
        lines = [x.strip() for x in lines]
        lines = [x for x in lines if x.strip()]
        for line in lines:
            line = line.split()
            if len(line) > dim:
                word = line[0]
                if word not in exists:
                    vec = np.array([float(i) for i in line[1:]])
                    vec = vec.reshape(1, dim)
                    vecs.append(vec)
                    words.append(word)
                    exists[word] = True

    embedding = np.concatenate(vecs)
    return words, embedding
