# -*- coding: utf-8 -*-
###############################################################################
# Copyright (c) 2014-2019 Mixlinker Networks Inc. <mixiot@mixlinker.com>
# All rights reserved.
#
# This program and the accompanying materials are made available under the
# terms of the Application License of Mixlinker Networks License and Mixlinker
# Distribution License which accompany this distribution.
#
# The Mixlinker License is available at
#    http://www.mixlinker.com/legal/license.html
# and the Mixlinker Distribution License is available at
#    http://www.mixlinker.com/legal/distribution.html
#
# Contributors:
#    Mixlinker Technical Team
###############################################################################
# Description : 固定化的参数
# Author : zhaoguangjun
class Config():
    ## train and test
    model_path = "best_model_i5_o1-S47.pkl"
    batch_size = 64
    epochs = 200    
    optimizers = "sgd"
    learning_rate = 1e-5
    beta1 = 0.5
    idx = 1092990

    ## data
    map_name = "./DEVICE1017_map.csv "  
    train_file = "./train_SK.csv"    
    test_file = "./test_SK.csv"
    max_read_len = 900000
    in_keys = ["SK", "S12", "S09", "S33", "S21"]
    out_keys = ["S47"]
    
    ## model
    in_class = len(in_keys)
    out_class = len(out_keys)
    hidden_dim = 2048



