#! /usr/bin/env python3

import tensorflow as tf
import pandas as pd
import numpy as np
import os

from tqdm import tqdm

from thainlplib import ThaiWordSegmentLabeller
from thainlplib.model import ThaiWordSegmentationModel

DIR = "/".join(__file__.split("/")[:-1])
SAVED_MODEL_PATH = '%s/saved_model' % DIR
TMP_FILE = '.tmptfrecord'

session = tf.Session(config=tf.ConfigProto(log_device_placement=True))

model = tf.saved_model.loader.load(session, [tf.saved_model.tag_constants.SERVING], SAVED_MODEL_PATH)
signature = model.signature_def[tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]
graph = tf.get_default_graph()

g_inputs = graph.get_tensor_by_name(signature.inputs['inputs'].name)
g_lengths = graph.get_tensor_by_name(signature.inputs['lengths'].name)
g_training = graph.get_tensor_by_name(signature.inputs['training'].name)
g_outputs = graph.get_tensor_by_name(signature.outputs['outputs'].name)

def nonzero(a):
    return [i for i, e in enumerate(a) if e != 0]

def split(s, indices):
    return [s[i:j] for i,j in zip(indices, indices[1:]+[None])]

def tokenize(sentence):

    inputs = [ThaiWordSegmentLabeller.get_input_labels(sentence)]
    lengths = [len(sentence)]

    y = session.run(g_outputs, feed_dict={
        g_inputs: inputs,
        g_lengths: lengths,
        g_training: False
    })

    indices = nonzero(y) if y[0] == 1 else [0] + nonzero(y)

    return split(sentence, indices)
