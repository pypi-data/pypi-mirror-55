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
# Description : 锅炉生产参数预测模型框架
# Author : zhaoguangjun

import torch.nn as nn
from .config import Config

class Net(nn.Module):
    def __init__(self, in_class=None, hidden_dim=None, out_class=None):
        self.in_class = in_class
        self.out_class = out_class
        self.hidden_dim = hidden_dim
        super(Net, self).__init__()

        self.conv1 = nn.Conv1d(in_channels=self.in_class, out_channels=self.hidden_dim, kernel_size=1, stride=1)
        self.bn1 = nn.BatchNorm1d(self.hidden_dim)
        self.relu1 = nn.LeakyReLU(inplace=True)

        self.conv2 = nn.Conv1d(in_channels=self.hidden_dim, out_channels=self.hidden_dim, kernel_size=1, stride=1)
        self.bn2 = nn.BatchNorm1d(self.hidden_dim)
        self.relu2 = nn.LeakyReLU(inplace=True)

        self.conv3 = nn.Conv1d(in_channels=self.hidden_dim, out_channels=self.out_class, kernel_size=1, stride=1)

    def forward(self, x):
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu1(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu2(out)

        output = self.conv3(out).view(out.size(0), -1)
        return output
