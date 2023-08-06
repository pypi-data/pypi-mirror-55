# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


from predict_helper import get_predict_args_parser

if __name__ == "__main__":
    parser = get_predict_args_parser()
    parser.parse_args()
