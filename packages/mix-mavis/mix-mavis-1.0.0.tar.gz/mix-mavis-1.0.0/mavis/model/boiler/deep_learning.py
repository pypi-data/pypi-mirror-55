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
# Description : 基于深度学习的锅炉生产参数预测模型训练
# Author : zhaoguangjun

import numpy as np
import pandas as pd
import os
import ipywidgets as widgets
from ipywidgets import interact_manual
from datetime import datetime, timedelta
from IPython.core.interactiveshell import InteractiveShell
from itertools import product, chain
from pandas.plotting import register_matplotlib_converters
import torch
import torch.nn as nn
from torch.utils import data
from .net import Net
from .data_read import Read_data
import torch.optim as optim
from .config import Config
from .draw import Draw

register_matplotlib_converters(np.datetime64)

pd.options.display.max_rows = 30
pd.options.display.max_columns = 25
interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


def weights_init(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        m.weight.data.normal_(0.0, 0.02)
    elif classname.find('BatchNorm') != -1:
        m.weight.data.normal_(1.0, 0.02)
        m.bias.data.fill_(0)


def adjust_learning_rate(optimizer, num_epoch, factor=0.9, step=10):
    """Sets the learning rate to the initial LR decayed by "factor" every "step" epochs"""
    for param_group in optimizer.param_groups:
        param_group['lr'] = param_group['lr'] * (factor ** (num_epoch // step))


class Boiler(object):
    def __init__(self, data):
        self.data = data

    def __call__(self):
        print("数据预处理中")
        self.preprocessing()
        print("数据加工完成")
        return interact_manual(self.set_tuning,
                               tunning=widgets.Checkbox(value=False, description='启用超参数调试', disabled=False))

    def preprocessing(self):
        pass

    def moment_set(self, batch_size, epochs):
        return interact_manual(self.tuning,
                               batch_size_range=batch_size,
                               epochs=epochs,
                               learning_rate_range=widgets.FloatRangeSlider(
                                   value=[0.01, 0.1], min=1e-8, max=1, step=0.01, description='学习率',
                                   disabled=False),
                               moment_range=widgets.FloatRangeSlider(value=[0.5, 0.9922], min=0.5, max=0.9922,
                                                                     step=0.01,
                                                                     description='动量', disabled=False),
                               hidden_dim_range=widgets.IntRangeSlider(value=[128, 4096], min=128, max=4096, step=512,
                                                                       description='模型隐藏层', disabled=False),
                               )

    def set_tuning(self, tunning):
        if tunning:
            return interact_manual(self.tuning,
                                   batch_size_range=widgets.SelectionRangeSlider(
                                       options=np.linspace(2, 128, 64, dtype=np.int64),
                                       index=(0, 63),
                                       description='单次数据读取量',
                                       disabled=False),
                                   epochs=widgets.IntText(value=30, description='遍历数据集次数', disabled=False),
                                   learning_rate_range=widgets.FloatRangeSlider(
                                       value=[1e-8, 0.99], min=1e-8, max=1, step=0.00001,
                                       description='学习率',
                                       disabled=False),
                                   moment_range=widgets.FloatRangeSlider(value=[0.5, 0.9922], min=0.5, max=0.9922,
                                                                         step=0.01,
                                                                         description='动量', disabled=False),
                                   hidden_dim_range=widgets.IntRangeSlider(value=[128, 4096], min=128, max=4096,
                                                                           step=512,
                                                                           description='模型隐藏层',
                                                                           disabled=False),
                                   inkeys=widgets.SelectMultiple(
                                       options=self.data.columns.tolist(),
                                       value=self.data.columns[2:3].tolist(),
                                       description='输入数据',
                                       disabled=False
                                   ),
                                   outkeys=widgets.SelectMultiple(
                                       options=self.data.columns.tolist(),
                                       value=self.data.columns[3:4].tolist(),
                                       description='输出数据',
                                       disabled=False
                                   ),
                                   )
        else:
            return interact_manual(self.fit,
                                   batch_size=widgets.IntText(value=10, description='单次数据读取',
                                                              disabled=False),
                                   epochs=widgets.IntText(value=30, description='遍历数据集次数', disabled=False),
                                   learning_rate=widgets.FloatText(value=0.1, description='学习率',
                                                                   disabled=False),
                                   moment=widgets.FloatText(value=0.9, description='动量', disabled=False),
                                   hidden_dim=widgets.IntText(value=1024, description='模型隐藏层',
                                                              disabled=False),
                                   inkeys=widgets.SelectMultiple(
                                       options=self.data.columns.tolist(),
                                       value=self.data.columns[2:3].tolist(),
                                       description='输入数据',
                                       disabled=False
                                   ),
                                   outkeys=widgets.SelectMultiple(
                                       options=self.data.columns.tolist(),
                                       value=self.data.columns[3:4].tolist(),
                                       description='输出数据',
                                       disabled=False
                                   ),
                                   )

    def tuning(self, batch_size_range, epochs, learning_rate_range, moment_range, hidden_dim_range, inkeys, outkeys):
        start_time = datetime.now()
        batch_size_list = chain(range(batch_size_range[0], batch_size_range[1], 2), (batch_size_range[1],))
        learning_rate_list = chain(np.arange(learning_rate_range[0], learning_rate_range[1], 0.01),
                                   (learning_rate_range[1],))
        hidden_dim_list = chain(range(hidden_dim_range[0], hidden_dim_range[1], 1), (hidden_dim_range[1],))
        moment_list = chain(np.arange(moment_range[0], moment_range[1], 0.01), (moment_range[1],))

        # cores = multiprocessing.cpu_count()
        # p = multiprocessing.Pool(cores)
        # product_list = product([epochs], learning_rate_list, batch_size_list, moment_list, hidden_dim_list)
        # print(product_list)
        # results = p.starmap(self.train, product_list)
        # p.close()
        # p.join()

        results = []
        for lr in learning_rate_list:
            for batch in batch_size_list:
                for moment in moment_list:
                    for hidd in hidden_dim_list:
                        results.append(self.train(epochs, lr, batch, moment, hidd, inkeys, outkeys))
        results_df = pd.DataFrame(results, columns=['训练集结果', '验证集结果', '遍历数据集次数', '学习率',
                                                    '单次数据读取量', '动量'])
        end_time = datetime.now()
        print('总耗时: ', end_time - start_time)
        results_df.to_csv('results_df.csv')
        return results_df

    def train(self, epochs, learning_rate, batch_size, moment, hidden_dim, inkeys, outkeys, l2=False):
        """
        此处的输入参数需要和tuning中的product_list一一对应.
        且此处optimizer中weight_decay已经被固定,如有需要可以传参.
        损失函数loss_fn被固定,可改写传参.
        :param epochs:
        :param learning_rate:
        :param batch_size:
        :param moment:
        :return:
        """

        print(inkeys, len(inkeys))
        print(outkeys, len(outkeys))
        net = Net(in_class=len(inkeys), hidden_dim=hidden_dim, out_class=len(outkeys))
        train_data = Read_data(self.data, mode="train", in_keys=inkeys, out_keys=outkeys)
        train_loader = data.DataLoader(train_data, batch_size=batch_size, shuffle=False, num_workers=4)
        optimizer = optim.SGD(params=net.parameters(), lr=learning_rate, momentum=moment, weight_decay=2e-5)
        lr_schedule = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.3, verbose=True, patience=5)
        loss_fn = nn.MSELoss()
        lowest_loss = 50000
        net.train()
        for epoch in range(epochs):
            total_loss = 0
            for t, (x, y) in enumerate(train_loader):
                optimizer.zero_grad()
                x = torch.unsqueeze(x, 2).float()
                output = net(x)
                # L2正则化
                if l2:
                    regularization_loss = 0
                    for param in net.parameters():
                        regularization_loss += torch.sum(abs(param))
                    loss = loss_fn(output, y.float()) + 0.5 * regularization_loss
                else:
                    loss = loss_fn(output, y.float())
                loss.backward()
                optimizer.step()
                total_loss += loss
                avg_loss = total_loss / (t + 1)
                if (t + 1) % 10 == 0:
                    print('epoch : %d / %d, iter: %d, average loss is: %.6f, batch loss: %.6f' % (
                        epoch + 1, epochs, t, avg_loss, loss))
            adjust_learning_rate(optimizer, epoch + 1, step=10)
            if avg_loss < lowest_loss:
                lowest_loss = avg_loss
                print('saving model .......')
                if not os.path.exists(Config.model_path):
                    os.makedirs(Config.model_path)
                torch.save(net, os.path.join(Config.model_path, "best_model.pkl"))
                print('finished saving model!')
            val_loss = self.validation(net, batch_size, inkeys, outkeys)
            lr_schedule.step(val_loss)
        return [avg_loss, val_loss] + [epochs, learning_rate, batch_size, moment, hidden_dim]

    def validation(self, net, batch_size, inkeys, outkeys):
        val_data = Read_data(self.data, mode='val', inkeys=inkeys, outkeys=outkeys)
        val_loader = data.DataLoader(val_data, batch_size=batch_size, shuffle=False, num_workers=4)
        net.eval()
        total_loss = 0
        for i, (x, y) in enumerate(val_loader):
            with torch.no_grad():
                x = torch.unsqueeze(x, 2).float()
                out = net(x)
                loss = self.loss_func(out, y.float())
                total_loss += loss.item()
        val_loss = total_loss / (len(val_data))
        print("validation loss is : %.5f", val_loss)
        return val_loss

    def fit(self, batch_size, epochs, learning_rate, moment, hidden_dim, inkeys, outkeys):
        return self.train(epochs=epochs, learning_rate=learning_rate, batch_size=batch_size, moment=moment,
                          hidden_dim=hidden_dim, inkeys=inkeys, outkeys=outkeys)