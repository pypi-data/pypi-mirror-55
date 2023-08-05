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
# Description : 基于Iforest的异常检测算法
# Author : kanxiangyang

import numpy as np
import pandas as pd
import ipywidgets as widgets
from ipywidgets import interact_manual
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import multiprocessing
from datetime import datetime, timedelta
from IPython.core.interactiveshell import InteractiveShell
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from itertools import product, chain
from ast import literal_eval
import _pickle as cPickle
from pandas.plotting import register_matplotlib_converters
# import mavis
# import threading
# import requests
# import json
# import time
# from IPython.display import clear_output


register_matplotlib_converters(np.datetime64)

pd.options.display.max_rows = 30
pd.options.display.max_columns = 25
interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


class IForest(object):
    def __init__(self, data):
        self.data = data
        self.mean = None
        self.std = None
        self.interval = 60
        self.result = pd.DataFrame()

    def __call__(self):
        print("数据预处理中")
        self.preprocessing()
        print("数据加工完成")
        return interact_manual(self.set_tuing,
                               tuning=widgets.Checkbox(value=False, description='启用超参数调试', disabled=False))

    def preprocessing(self):
        self.data = self.data.dropna(axis=1, how='all')
        self.data = self.data.dropna(axis=0, how='any')
        self.mean = self.data.mean(axis=0)
        std = self.data.std(axis=0)
        constant_col = std[std < 1e-6].index.tolist()
        std[constant_col] = 1
        self.std = std
        self.data -= self.mean
        self.data /= self.std

    def set_tuing(self, tuning):
        if tuning:
            return interact_manual(self.tuning,
                                   n_estimators_range=widgets.IntRangeSlider(
                                       value=[100, 100], min=100, max=1000, step=100, description='基学习器数量: ',
                                       disabled=False),
                                   max_samples_range=widgets.SelectionRangeSlider(
                                       options=list(np.exp2(range(4, 12)).astype('int')), index=(4, 6),
                                       description='最大叶样本数: ', disabled=False),
                                   max_features_range=widgets.FloatRangeSlider(
                                       value=[0.5, 0.9], min=0, max=1, step=0.1, description='最大叶特征比例: ',
                                       disabled=False),
                                   contamination=widgets.FloatLogSlider(
                                       value=1e-3, min=-6, max=-1, base=10, description='异常比例: ', disabled=False)
                                   )
        else:
            return interact_manual(self.fit,
                                   n_estimators=widgets.Text(value='100', description='基学习器数量', disabled=False),
                                   max_samples=widgets.Text(value='auto', description='最大叶样本数', disabled=False),
                                   max_features=widgets.Text(value='1.0', description='最大叶特征比例', disabled=False),
                                   contamination=widgets.Text(value='0.1', description='异常比例', disabled=False)
                                   )

    def train(self, n_estimators, max_samples, max_features, contamination):
        x_train, x_validation = train_test_split(self.data, test_size=0.2, shuffle=False)
        model = IsolationForest(n_estimators=n_estimators, max_samples=n_estimators, max_features=max_features,
                                contamination=contamination, behaviour='new',
                                random_state=30, verbose=True)
        model.fit(x_train)
        score_anomalies_train = model.decision_function(x_train)
        score_anomalies_validation = model.decision_function(x_validation)
        score_train = pd.Series(score_anomalies_train, index=x_train.index)
        score_validation = pd.Series(score_anomalies_validation, index=x_validation.index)
        ewm_score_train = (x_train - x_train.ewm(com=9).mean()).apply(lambda x: np.linalg.norm(x), axis=1)
        ewm_score_validation = (x_validation - x_validation.ewm(com=9).mean()).apply(lambda x: np.linalg.norm(x),
                                                                                     axis=1)
        metrics_train = np.corrcoef(ewm_score_train, score_train)[0, 1]
        metrics_validation = np.corrcoef(ewm_score_validation, score_validation)[0, 1]
        return [metrics_train, metrics_validation] + [n_estimators, max_samples, max_features, contamination]

    def tuning(self, n_estimators_range, max_samples_range, max_features_range, contamination):
        start_time = datetime.now()
        n_estimators_list = chain(range(n_estimators_range[0], n_estimators_range[1], 100), (n_estimators_range[1],))
        max_features_list = chain(np.arange(max_features_range[0], max_features_range[1], 0.1),
                                  (max_features_range[1],))

        cores = multiprocessing.cpu_count()
        p = multiprocessing.Pool(cores)
        product_list = product(n_estimators_list, max_samples_range, max_features_list, [contamination])
        results = p.starmap(self.train, product_list)
        p.close()
        p.join()
        results_df = pd.DataFrame(results, columns=['训练集结果', '验证集结果', '基学习器数量', '最大叶样本数',
                                                    '最大叶特征比例', '异常比例'])
        mpl.rcParams["figure.figsize"] = [8, 8]
        g = sns.FacetGrid(results_df, col='最大叶样本数', col_wrap=1)
        g.map(plt.plot, '最大叶特征比例', '训练集结果', label='训练集', marker=".", color='b', alpha=.7).set_axis_labels(
            '最大叶特征比例', '结果')
        g.map(plt.plot, '最大叶特征比例', '验证集结果', label='验证集', marker=".", color='r', alpha=.7).set_axis_labels(
            '最大叶特征比例', '结果')
        g.add_legend()
        end_time = datetime.now()
        print('总耗时: ', end_time - start_time)
        results_df.to_csv('results_df.csv')
        return results_df

    def fit(self, n_estimators, max_samples, max_features, contamination):
        n_estimators = literal_eval(n_estimators)
        if max_samples is not 'auto':
            max_samples = literal_eval(max_samples)
        max_features = literal_eval(max_features)
        contamination = literal_eval(contamination)
        model = IsolationForest(n_estimators=n_estimators, max_samples=max_samples, max_features=max_features,
                                contamination=contamination, n_jobs=-1, behaviour='new', random_state=42, verbose=True)
        model.fit(self.data)
        with open('iforest.pkl', 'wb') as f:
            cPickle.dump(model, f)

    # def predict(self):
    #
    #
    # def _predict(self, ):
    #     while True:
    #         clear_output(wait=True)
    #         plt.figure(figsize=(16, 8))
    #         mavis.get_data(url="")
    #         plt.plot(self.result)
    #         plt.title('实时异常分数')
    #         plt.grid(True)
    #         plt.show()
    #         time.sleep(self.interval)

    # def pump(self, url, authorization, device, interval):
    #     self.interval = literal_eval(interval)
    #     time_now = datetime.now()
    #     start_time = (time_now - timedelta(seconds=self.interval)).strftime('%Y-%m-%d %H:%M:%S')
    #     end_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
    #     parameter = {'equipment_id': device, 'page_size': '10', 'page_index': '1',
    #                  'end_time': str(end_time), 'start_time': str(start_time), 'keys': self.keys}
    #     response = requests.post(url=url, headers={'Authorization': authorization}, data=parameter)
    #     json_data = json.loads(response.content)['result']['data']
    #     if not json_data:
    #         print('查询为空')
    #     response.close()
    #     time_index = pd.to_datetime([j['time'] for j in json_data])
    #     df = pd.DataFrame([j['value'] for j in json_data], index=time_index, columns=self.columns)
    #     df -= self.mean
    #     df /= self.std
    #     df = df.mean(axis=0).to_frame().T
    #     df.index = [time_index[0]]
    #     with open('iforest.pkl', 'rb') as f:
    #         model = cPickle.load(f)
    #     self.result = self.result.append(pd.Series(model.decision_function(df), index=[time_index[0]]))
    #     self.result.name = 'score'
    #     print('success:', time.ctime())
    #
    # def timer(self, url, authorization, device, interval):
    #     global t
    #     t = threading.Timer(interval=self.interval, function=self.pump,
    #                         kwargs={url: url, authorization: authorization, device: device, interval: interval})
    #     t.start()
    #
    # def interact_pump(self):
    #     return interact_manual(self.timer,
    #                            url=widgets.Text(
    #                                value='http://pro.sunevap.mixiot.top/pro/equipment/public_get_mosaic_by_key',
    #                                description='请求地址', disabled=False),
    #                            authorization=widgets.Text(value='bear xxxxx', description='认证', disabled=False),
    #                            device=widgets.Text(value='', description='设备ID', disabled=False),
    #                            interval=widgets.Text(value='10', description='时间间隔/s', disabled=False)
    #                            )
    #
    # def live_plot(self):
    #     clear_output(wait=True)
    #     plt.figure(figsize=(16, 8))
    #     plt.plot(self.result)
    #     plt.title('实时异常分数')
    #     plt.grid(True)
    #     plt.show()
    #
    # def predict(self):
    #     while True:
    #         self.live_plot()
    #         time.sleep(self.interval)
