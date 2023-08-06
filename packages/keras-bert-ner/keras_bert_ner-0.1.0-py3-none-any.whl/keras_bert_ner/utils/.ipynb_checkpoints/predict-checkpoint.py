# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import codecs
import pickle
import numpy as np
from keras.models import load_model
from bert4keras.layers import custom_objects
from bert4keras.utils import Tokenizer
from ..decode.viterbi import Viterbi
from keras_contrib.layers import CRF
from ..train.crf_utils import CRF_Accuracy, CRF_Loss


__all__ = ["build_trained_model", "get_model_inputs"]


def build_trained_model(args):
    if args.device_map != "cpu":
        os.environ["CUDA_VISIBLE_DEVICES"] = args.device_map
    else:
        os.environ["CUDA_VISIBLE_DEVICES"] = ""
    
    token_dict = {}
    with codecs.open(args.bert_vocab, "r", encoding="utf-8") as f:
        for line in f:
            token = line.strip()
            token_dict[token] = len(token_dict)
    
    tokenizer = Tokenizer(token_dict)
    
    with codecs.open(os.path.join(args.model_path, "tag2id.pkl"), "rb") as f:
        tag2id = pickle.load(f)
    with codecs.open(os.path.join(args.model_path, "id2tag.pkl"), "rb") as f:
        id2tag = pickle.load(f)
        
    mask_tag = "X"
    crf_loss = CRF_Loss(tag2id=tag2id, mask_tag=mask_tag).crf_loss
    crf_accuracy = CRF_Accuracy(tag2id=tag2id, mask_tag=mask_tag).crf_accuracy
    
    custom_objects["CRF"] = CRF
    custom_objects["crf_loss"] = crf_loss
    custom_objects["crf_accuracy"] = crf_accuracy
    
    model = load_model(os.path.join(args.model_path, args.model_name), custom_objects=custom_objects)
        
    viterbi_decoder = Viterbi(model, len(id2tag))
        
    return tokenizer, id2tag, viterbi_decoder

def get_model_inputs(tokenizer, src_data, max_len):
    tokens, segs = [], []
    for item in src_data:
        res = tokenizer.encode(item, first_length=max_len)
        tokens.append(np.array(res[0]))
        segs.append(np.array(res[1]))
    return tokens, segs