# -*- coding: UTF-8 -*-

import ipywidgets as widgets
from ipywidgets import interact_manual
from IPython.core.interactiveshell import InteractiveShell
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import product
import multiprocessing
from sklearn.model_selection import train_test_split

# matplotlib中文化支持
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['axes.unicode_minus'] = False

interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'

# 超参数调试
hyper_parameters = {
    'para1': {'description': '参数1', 'default': 0.1, 'range': np.float_power(10, range(-2, 3))},
    'para2': {'description': '参数2', 'default': 256, 'range': np.int32(np.exp2(range(7, 11)))},
    'para3': {'description': '参数3', 'default': 500, 'range': range(100, 600, 100)},
    'para4': {'description': '参数4', 'default': 0.999, 'range': [0.9, 0.99, 0.999, 0.9999]}
}

# fit交互模块
fit_kwargs = {k: widgets.Text(value=str(v['default']), description=v['description'], disabled=False) for k, v in
              hyper_parameters.items()}

# tuing交互模块
tuning_kwargs = {
    k + '_list': widgets.SelectionRangeSlider(options=[(v['range'][i], i) for i in range(len(v['range']))],
                                              index=(0, 1), description=v['description'],
                                              disabled=False) for k, v in hyper_parameters.items()}


class ModelDemo(object):
    def __init__(self, data):
        self.data = data
        self.mean = None
        self.std = None
        self.interval = 60

    def __call__(self):
        return interact_manual(self.set_tuing,
                               tuning=widgets.Checkbox(value=False, description='启用超参数调试', disabled=False)
                               )

    # 数据预处理
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
            return interact_manual(self.tuning, **tuning_kwargs)
        else:
            return interact_manual(self.fit, **fit_kwargs)

    def train(self, para1, para2, para3, para4):
        x_train, x_validation = train_test_split(self.data, test_size=0.2, shuffle=False)
        compare_vector_train = np.random.rand(1, 4) + np.log10(x_train.shape[0])
        compare_vector_validation = np.random.rand(1, 4) + np.log10(x_validation.shape[0])
        parameter_vector = [np.log10(para1), para2 // 128, para3 // 100, np.log10(1 - para4)]
        result_train = np.linalg.norm(compare_vector_train - parameter_vector)
        result_validation = np.linalg.norm(compare_vector_validation - parameter_vector)
        return [result_train, result_validation] + [para1, para2, para3, para4]

    def tuning(self, para1_list, para2_list, para3_list, para4_list):
        for k in hyper_parameters.keys():
            v = locals()[k + '_list']
            hyper_parameters[k].update({'list': hyper_parameters[k]['range'][v[0]:v[1] + 1]})
            hyper_parameters[k].update({'list_length': v[1] - v[0] + 1})
        hyper_df = pd.DataFrame.from_dict(hyper_parameters, orient='index')
        if hyper_df[hyper_df['list_length'] != 1].shape[0] > 2:
            print('一口吃不成胖子，一步跨不到天边，最多同时调两个参数，谢谢')
            raise Exception
        cores = multiprocessing.cpu_count()
        p = multiprocessing.Pool(cores)
        product_list = product(*hyper_df['list'].tolist())
        results = p.starmap(self.train, product_list)
        p.close()
        p.join()
        tuning_params = hyper_df[hyper_df['list_length'] != 1]['description'].tolist()
        columns = ['训练集结果', '验证集结果'] + hyper_df['description'].tolist()
        results_df = pd.DataFrame(results, columns=columns)
        if len(tuning_params) == 2:
            nums_1 = hyper_df.loc[hyper_df[hyper_df['description'] == tuning_params[0]].index[0], 'list_length']
            mpl.rcParams["figure.figsize"] = [10, 6 * nums_1]
            fig_1, axes_1 = plt.subplots(nrows=nums_1)
            for idx, (value, split_df) in enumerate(results_df.groupby(tuning_params[0])):
                split_df.index = split_df[tuning_params[1]]
                split_df = split_df[['训练集结果', '验证集结果']]
                ax = sns.lineplot(data=split_df, markers=True, ax=axes_1[idx])
                ax.grid(True)
                ax.set_title(f"{tuning_params[0]}: {value}")
            nums_2 = hyper_df.loc[hyper_df[hyper_df['description'] == tuning_params[1]].index[0], 'list_length']
            mpl.rcParams["figure.figsize"] = [10, 6 * nums_2]
            fig_2, axes_2 = plt.subplots(nrows=nums_2)
            for idx, (value, split_df) in enumerate(results_df.groupby(tuning_params[1])):
                split_df.index = split_df[tuning_params[0]]
                split_df = split_df[['训练集结果', '验证集结果']]
                ax = sns.lineplot(data=split_df, markers=True, ax=axes_2[idx])
                ax.grid(True)
                ax.set_title(f"{tuning_params[1]}: {value}")
        else:
            mpl.rcParams["figure.figsize"] = [12, 8]
            results_df.index = results_df[tuning_params[0]]
            results_df = results_df[['训练集结果', '验证集结果']]
            ax = sns.lineplot(data=results_df, markers=True)
            ax.grid(True)
        return results_df

    def fit(self, para1, para2, para3, para4):
        print('DEMO 演示')
        print(self.data.head(), para1, para2, para3, para4)
