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
# Description : mavis核心功能
# Author : kanxiangyang

import pandas as pd
import ipywidgets as widgets
import boto3
import os
from ipywidgets import interact, interact_manual
from IPython.core.interactiveshell import InteractiveShell
from .transfer import read
from .plot import MavisPlot
from . import config

interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


class Analysis(object):
    def __init__(self):
        self.whole_file = None
        self.fileframe = None
        self.directory = None
        self.count = None
        self.last_record = None
        self.max_length = None
        self.data = None
        self.preview_repository = None
        self.model_repository = None

    def select_preview(self, plot):
        mv = MavisPlot(self.data)
        return getattr(mv, self.preview_repository[plot])()

    def select_model(self, model):
        # 调用模型和数据
        module_mavis = __import__("mavis")
        model_class = getattr(module_mavis, config.model_repository[model])
        model_class(self.data)()

    def select_filename(self, preview):
        filename_split = self.directory.rsplit('/', 1)
        self.data = read(filename_split[0], filename_split[1])
        if preview:
            self.preview_repository = config.preview_repository
            return interact_manual(self.select_preview,
                                   plot=widgets.Dropdown(options=list(self.preview_repository.keys()),
                                                         value=list(self.preview_repository.keys())[0],
                                                         description='可视化库 '))
        else:
            self.model_repository = config.model_repository
            return interact_manual(self.select_model,
                                   model=widgets.Dropdown(options=list(self.model_repository.keys()),
                                                          value=list(self.model_repository.keys())[0],
                                                          description='算法库 '))

    def select_directory(self, directory):
        # 判断目录选择的递归函数回到了第几层
        if self.last_record:
            self.fileframe = self.whole_file
            for col in range(len(self.last_record)):
                if {directory, self.last_record[col]}.issubset(self.fileframe.iloc[:, col].unique()):
                    self.count = col
                    self.directory = os.path.join(*self.last_record[:col]) if col > 0 else None
                    for i in range(col):
                        self.fileframe = self.fileframe[self.fileframe[i] == self.last_record[i]]
                    break
                else:
                    pass
        if not self.directory:
            self.directory = directory
        else:
            self.directory = self.directory + '/' + directory
        self.fileframe = self.fileframe[self.fileframe[self.count] == directory]
        self.count += 1
        if not self.fileframe.iloc[:, self.count:].any(axis=None):
            self.last_record = self.directory.split('/')
            return interact_manual(self.select_filename,
                                   preview=widgets.Checkbox(value=False, description='是否预览数据', disabled=False))
        else:
            self.last_record = None
            directory_list = self.fileframe[self.count].unique().tolist()
            if '' in directory_list:
                directory_list.remove('')
            return interact(self.select_directory,
                            directory=widgets.Dropdown(options=directory_list, value=directory_list[0],
                                                       description='子目录 '))

    def __call__(self, ):
        self.fileframe = pd.DataFrame(
            [f['Key'].split('/') for f in boto3.client("s3").list_objects(Bucket='mixiot')['Contents']])
        self.whole_file = self.fileframe
        self.max_length = self.whole_file.shape[1]
        self.count = 0
        directory_list = self.fileframe[self.count].unique().tolist()
        return interact(self.select_directory,
                        directory=widgets.Dropdown(options=directory_list, value=directory_list[0],
                                                   description='数据仓库目录 '))
