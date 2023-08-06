# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
from ..decode.viterbi import Viterbi
from keras.utils import to_categorical
from keras.callbacks import Callback, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

__all__ = ["NER_Callbacks", "Accuracy"]

class NER_Callbacks(object):
    
    def __init__(self, id2tag, mask_tag=None):
        self.callbacks = [Accuracy(id2tag, mask_tag)]
    
    def best_fit_callbacks(self, callback_configs):
        # add best-fit callbacks
        early_stop_patience = callback_configs.get("early_stop_patience")
        early_stopping = EarlyStopping(monitor="val_crf_accuracy", patience=early_stop_patience)
        self.callbacks.append(early_stopping)
        
        reduce_lr_patience = callback_configs.get("reduce_lr_patience")
        reduce_lr_factor = callback_configs.get("reduce_lr_factor")
        reduce_lr_on_plateau = ReduceLROnPlateau(monitor="val_crf_accuracy", verbose=1, mode="max", factor=reduce_lr_factor, patience=reduce_lr_patience)
        self.callbacks.append(reduce_lr_on_plateau)
        
        save_path = callback_configs.get("save_path")
        checkpoint = ModelCheckpoint(save_path, monitor="val_crf_accuracy", verbose=2, mode="max", save_best_only=True)
        self.callbacks.append(checkpoint)
        return self.callbacks

    def callbacks(self):
        return self.callbacks
    
class Accuracy(Callback):
    
    def __init__(self, id2tag, mask_tag=None):
        self.id2tag = id2tag
        self.numb_tags = len(self.id2tag)
        self.mask_tag = mask_tag
        self.mask_pos = {self.id2tag[key]:key for key in self.id2tag}.get(self.mask_tag)
    
    def on_epoch_end(self, epoch, logs=None):
        viterbi = Viterbi(self.model, self.numb_tags)
        val_true = np.squeeze(self.validation_data[2], axis=-1)
        mask = np.array(1. - to_categorical(val_true, self.numb_tags)[:, :, self.mask_pos]) if self.mask_pos else None
        val_pred = viterbi.decode([self.validation_data[0], self.validation_data[1]])
        self.get_acc(val_true, val_pred, mask) 
        
    def get_acc(self, val_true, val_pred, mask):
        assert isinstance(val_true, np.ndarray), "expect val_true to be np.ndarray, but got " + str(type(val_true))
        assert isinstance(val_pred, np.ndarray), "expect val_pred to be np.ndarray, but got " + str(type(val_pred))
        assert val_true.shape == val_pred.shape, "expect val_true and val_pred to have the same shape, but got " + str(val_true.shape) + " and " + str(val_pred.shape)
        all_sents = val_true.shape[0]
        right_sents = 0
        all_tags = {item:0 for item in self.id2tag.values() if item != self.mask_tag}
        right_tags = {item:0 for item in self.id2tag.values() if item != self.mask_tag}
        if self.mask_tag == None:
            for sent_true, sent_pred in zip(val_true, val_pred):
                if all(sent_true == sent_pred):
                    right_sents += 1
                for tag_true, tag_pred in zip(sent_true, sent_pred):
                    if tag_true == tag_pred:
                        right_tags[self.id2tag[tag_pred]] += 1
                    all_tags[self.id2tag[tag_true]] += 1
        else:
            for sent_true, sent_pred, sent_mask in zip(val_true, val_pred, mask):
                if all(sent_true*sent_mask == sent_pred*sent_mask):
                    right_sents += 1
                for tag_true, tag_pred, tag_mask in zip(sent_true, sent_pred, sent_mask):
                    if tag_mask == 0.:
                        continue
                    if tag_true == tag_pred:
                        right_tags[self.id2tag[tag_pred]] += 1
                    all_tags[self.id2tag[tag_true]] += 1
        sents_acc = right_sents / all_sents
        tags_acc = {item:right_tags[item]/all_tags[item] for item in right_tags}
        print("*"*25+" Sentence Accuracy "+"*"*25)
        print("\t\t{}\t\t{}\t\t{}\n".format("Right","All","Accuracy"))
        print("\t\t{}\t\t{}\t\t{}\n".format(right_sents,all_sents,sents_acc))
        print("*"*25+" Tag Accuracy "+"*"*25)
        print("\t\t{}\t\t{}\t\t{}\n".format("Right","All","Accuracy"))
        for tag in tags_acc:
            print("{}\t\t{}\t\t{}\t\t{}\n".format(tag,right_tags[tag],all_tags[tag],tags_acc[tag]))