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
# Description : 自定义数据获取模块
# Author : zhaoguangjun

import torch
from torch.utils import data
import numpy as np
from sklearn.model_selection import train_test_split


class Read_data(data.Dataset):
    def __init__(self, data, max_read_len=None, mode="train", in_keys=None, out_keys=None):
        self.max_read = max_read_len
        self.in_keys = in_keys
        self.out_keys = out_keys
        self.mode = mode
        if self.max_read:
            self.in_data = data.loc[:self.max_read, self.in_keys]
            self.out_data = data.loc[:self.max_read, self.out_keys]
        else:
            self.in_data = data.loc[:, self.in_keys]
            self.out_data = data.loc[:, self.out_keys]

        self.train_data, self.val_data, self.train_label, self.val_label = train_test_split(self.in_data, self.out_data,
                                                                                            test_size=0.33,
                                                                                            random_state=2)
        if self.mode == "train":
            self.in_data = self.train_data
            self.out_data = self.train_label
        else:
            self.in_data = self.val_data
            self.out_data = self.val_label
        self.in_data = self._pd2tensor(self.in_data, self.in_keys)
        self.out_data = self._pd2tensor(self.out_data, self.out_keys)

    def _pd2tensor(self, np_data, keys):
        tensor_map = torch.tensor(np.array(np_data[keys[0]]).reshape(-1, 1))
        for key in keys[1:]:
            tensor_map = torch.cat((tensor_map, torch.tensor(np.array(np_data[key]).reshape(-1, 1))), 1)
        return tensor_map

    def __getitem__(self, index):
        return self.in_data[index], self.out_data[index]

    def __len__(self):
        return self.in_data.size(0)

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
# Date : 2019-9-5
# Author : Zhao Guangjun


# import torch
# from torch.utils import data
# import numpy as np
# from config import Config
# import pandas as pd
#
#
# def pd2tensor(data, keys):
#     tensor_map = torch.tensor(np.array(data[keys[0]]).reshape(-1, 1))
#     for key in keys[1:]:
#         tensor_map = torch.cat((tensor_map, torch.tensor(np.array(data[key]).reshape(-1, 1))), 1)
#     return tensor_map
#
#
# class Read_data(data.Dataset):
#     def __init__(self, file_name=None, mode='train', max_read_len=None, in_keys=Config.in_keys,
#                  out_keys=Config.out_keys):
#         """
#
#         :param file_name:
#         :param mode:
#         :param map_name:
#         :param max_read_len:
#         :param in_keys:
#         :param out_keys:
#         """
#         self.file = file_name
#         self.mode = mode
#         self.max_read = max_read_len
#         self.in_keys = in_keys
#         self.out_keys = out_keys
#         super(Read_data, self).__init__()
#
#         if self.max_read:
#             self.in_data = pd.read_csv(self.file, sep=',', nrows=self.max_read, usecols=self.in_keys)
#             self.in_data = pd2tensor(self.in_data, self.in_keys)
#             if self.mode != "test":
#                 self.out_data = pd.read_csv(self.file, sep=',', nrows=self.max_read, usecols=self.out_keys)
#                 self.out_data = pd2tensor(self.out_data, self.out_keys)
#         else:
#             self.in_data = pd.read_csv(self.file, sep=',', usecols=self.in_keys)
#             self.in_data = pd2tensor(self.in_data, self.in_keys)
#             if self.mode != "test":
#                 self.out_data = pd.read_csv(self.file, sep=',', usecols=self.out_keys)
#                 self.out_data = pd2tensor(self.out_data, self.out_keys)
#
#     def __getitem__(self, index):
#         if self.mode == 'test':
#             return self.in_data[index]
#         else:
#             return self.in_data[index], self.out_data[index]
#
#     def __len__(self):
#         return self.in_data.size(0)
