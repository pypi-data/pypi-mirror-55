# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras import backend as K
from keras.losses import categorical_crossentropy
from keras.losses import sparse_categorical_crossentropy


class CRF_Accuracy(object):
    
    def __init__(self, tag2id, mask_tag=None):
        self.tag2id = tag2id
        self.mask_pos = self.tag2id.get(mask_tag)
        
    def _get_accuracy(self, y_true, y_pred, sparse_target=False):
        y_pred = K.argmax(y_pred, -1)
        mask = K.cast(1. - K.one_hot(K.squeeze(K.cast(y_true, "int32"), axis=-1), num_classes=len(self.tag2id))[:, :, self.mask_pos], K.floatx())
        if sparse_target:
            y_true = K.cast(y_true[:, :, 0], K.dtype(y_pred))
        else:
            y_true = K.argmax(y_true, -1)
        judge = K.cast(K.equal(y_pred, y_true), K.floatx())
        if self.mask_pos is None:
            return K.mean(judge)
        else:
            return K.sum(judge * mask) / K.sum(mask)
    
    def crf_viterbi_accuracy(self, y_true, y_pred):
        """Use Viterbi algorithm to get best path, and compute its accuracy.
        `y_pred` must be an output from CRF."""
        crf, idx = y_pred._keras_history[:2]
        X = crf._inbound_nodes[idx].input_tensors[0]
        y_pred = crf.viterbi_decoding(X, None)
        return self._get_accuracy(y_true, y_pred, crf.sparse_target)

    def crf_marginal_accuracy(self, y_true, y_pred):
        """Use time-wise marginal argmax as prediction.
        `y_pred` must be an output from CRF with `learn_mode="marginal"`"""
        crf, idx = y_pred._keras_history[:2]
        X = crf._inbound_nodes[idx].input_tensors[0]
        y_pred = crf.get_marginal_prob(X, None)
        return self._get_accuracy(y_true, y_pred, crf.sparse_target)

    def crf_accuracy(self, y_true, y_pred):
        """Get default accuracy based on CRF `test_mode`."""
        crf, idx = y_pred._keras_history[:2]
        if crf.test_mode == "viterbi":
            return self.crf_viterbi_accuracy(y_true, y_pred)
        else:
            return self.crf_marginal_accuracy(y_true, y_pred)
        
        
class CRF_Loss(object):
    
    def __init__(self, tag2id, mask_tag=None):
        self.tag2id = tag2id
        self.mask_pos = self.tag2id.get(mask_tag)
        
    def crf_nll(self, y_true, y_pred):
        """The negative log-likelihood for linear chain Conditional Random Field (CRF).
        
        This loss function is only used when the `layers.CRF` layer 
        is trained in the "join" mode.
        
        # Arguments
            y_true: tensor with true targets.
            y_pred: tensor with predicted targets.
            
        # Returns
            A scalar representing corresponding to the negative log-likelihood.
            
        # Raises
            TypeError: If CRF is not the last layer.
            
        # About Codes
            This code is from Keras-Team/keras_contrib.losses.crf_losses, 
            change some details.
        """
        
        crf, idx = y_pred._keras_history[:2]
        if crf._outbound_nodes:
            raise TypeError("When learn_model='join', CRF must be the last layer.")
        if crf.sparse_target:
            y_true = K.one_hot(K.cast(y_true[:, :, 0], "int32"), crf.units)
        X = crf._inbound_nodes[idx].input_tensors[0]
        mask = K.cast(1. - y_true[:, :, self.mask_pos], K.floatx()) if self.mask_pos else None
        nloglik = crf.get_negative_log_likelihood(y_true, X, mask)
        return nloglik
    
    def crf_loss(self, y_true, y_pred):
        """General CRF loss function depanding on the learning mode.
        
        # Arguments
            y_true: tensor with true targets.
            y_pred: tensor with predicted targets.
            
        # Returns
            If the CRF layer is being trained in the join mode, returns the negative
            log-likelihood. Otherwise returns the categorical crossentropy implemented
            by the underlying Keras backend.
            
        # About Codes
            This code is from Keras-Team/keras_contrib.losses.crf_losses, 
            change some details.
        """
        
        crf, idx = y_pred._keras_history[:2]
        if crf.learn_mode == "join":
            return self.crf_nll(y_true, y_pred)
        else:
            if crf.sparse_target:
                return sparse_categorical_crossentropy(y_true, y_pred)
            else:
                return categorical_crossentropy(y_true, y_pred)