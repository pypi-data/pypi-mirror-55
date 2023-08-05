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
# Description : 数据可视化
# Author : kanxiangyang

import pandas as pd
from scipy import stats
import ipywidgets as widgets
from ipywidgets import interact_manual
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display, FileLink
from .api import create_download_link
import os

# matplotlib中文化支持
mpl.rcParams['font.sans-serif'] = ['simhei']
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['axes.unicode_minus'] = False

# 展示的最大行数
pd.options.display.max_rows = 10

# 展示的最大列数
pd.options.display.max_columns = 10

# 交互设置
interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


def set_figsize(length, width):
    """
    设置数据展示图大小

    :param str length: 图的长度
    :param str width: 图的宽度
    """
    mpl.rcParams["figure.figsize"] = [length, width]


class MavisPlot(pd.DataFrame):
    """
    数据预览与交互式可视化

    展示数据的基本统计量, 缺失值分析, 单参数趋势图, 单参数分布图, 单参数PP图，双参数散点图, 多参数关系图，多参数相关性热点图等信息

    :param data: 数据所在本地路径或DataFrame
    """

    def __init__(self, data):
        if isinstance(data, str):
            if data.endswith('.csv'):
                data = pd.read_csv(data, index_col=0, parse_dates=True).sort_index(axis=0, ascending=True)
            elif data.endswith('.h5'):
                data = pd.read_hdf(data).sort_index(axis=0, ascending=True)
            else:
                raise IOError('路径格式错误，请输入csv格式或h5格式')
        else:
            pass
        super().__init__(data=data)
        self.index = pd.to_datetime(self.index)

    def summary(self):
        """
        数据基本统计量, 包括

        样本数

        平均值

        标准差

        最小值

        1/4位数

        中位数

        3/4位数

        最大值
        """
        preview_df = self.describe().T
        preview_df.columns = ['样本数', '平均值', '标准差', '最小值', '1/4位数', '中位数', '3/4位数', '最大值']
        preview_df['偏度'] = self.skew()
        preview_df['峰度'] = self.kurt()
        filename = "data/preview_statistics.csv"
        if not os.path.exists("data/"):
            os.makedirs("data/")
        preview_df.to_csv(filename, encoding='utf_8_sig')
        print(f'参数基本统计量表:\n')
        # categorical_columns = self.columns[self.apply(lambda x: x.value_counts().shape[0] < 3, axis=0)].tolist()
        # print(f'0-1型状态参数：\n{categorical_columns}')
        display(FileLink(filename))
        return create_download_link(preview_df, title="下载到本地", filename=filename)

    def _naplot(self, columns, start_date, end_date, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        naplot_df = self.loc[(self.index >= start_date) & (self.index <= end_date)][list(columns)]
        percent_col = naplot_df.isnull().sum().sort_values(ascending=False) / naplot_df.shape[0]
        plt.subplots(figsize=(12, 6))
        plt.xticks(rotation='90')
        sns.barplot(x=list(columns), y=percent_col)
        plt.xlabel('参数', fontsize=15)
        plt.ylabel('缺失值比例', fontsize=15)
        plt.title('各参数的缺失值比例', fontsize=15)
        if save:
            plt.savefig("参数缺失情况.png", dpi=600)

    def naplot(self):
        """
        数据缺失值比例图

        :param list columns: 分析的参数列表
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns_list = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def naplot_demo(columns, start_date, end_date, save=False):
                print('demo')

            interact_manual(naplot_demo,
                            columns=widgets.SelectMultiple(options=columns_list, value=columns_list[0:2],
                                                           description='多参数选择'),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            数据缺失值比例图')
        return interact_manual(self._naplot,
                               columns=widgets.SelectMultiple(options=self.columns.tolist(),
                                                              value=self.columns[0:2].tolist(),
                                                              description='多参数选择'),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _timeplot(self, column, start_date, end_date, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        timeplot_df = self.loc[(self.index >= start_date) & (self.index <= end_date)][column]
        set_figsize(10, 5)
        timeplot_df.plot()
        if save:
            plt.savefig(f"参数{column}的趋势图.png", dpi=600)

    def timeplot(self):
        """
        单参数趋势图

        :param str column: 分析参数
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def timeplot_demo(column, start_date, end_date, save=False):
                print()

            interact_manual(timeplot_demo,
                            column=widgets.Dropdown(options=columns, value=columns[0], description='参数: '),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            单参数趋势图')
        return interact_manual(self._timeplot,
                               column=widgets.Dropdown(options=list(self.columns), value=self.columns[0],
                                                       description='参数: '),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _distplot(self, column, start_date, end_date, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        distplot_df = self.loc[(self.index >= start_date) & (self.index <= end_date)][column]
        set_figsize(10, 5)
        sns.distplot(distplot_df)
        if save:
            plt.savefig(f"参数{column}的分布图.png", dpi=600)

    def distplot(self):
        """
        单参数分布图

        :param str column: 分析参数
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def distplot_demo(column, start_date, end_date, save=False):
                print()

            interact_manual(distplot_demo,
                            column=widgets.Dropdown(options=columns, value=columns[0], description='参数: '),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            单参数分布图')
        return interact_manual(self._distplot,
                               column=widgets.Dropdown(options=list(self.columns), value=self.columns[0],
                                                       description='参数: '),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _probplot(self, column, start_date, end_date, boxcox, lmbda, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        probplot_df = self.loc[(self.index >= start_date) & (self.index <= end_date)][column]
        set_figsize(10, 5)
        if boxcox:
            stats.probplot(stats.boxcox(probplot_df, lmbda=lmbda), plot=plt)
        else:
            stats.probplot(probplot_df, plot=plt)
        if save:
            plt.savefig(f"参数{column}的PP图.png", dpi=600)

    def probplot(self):
        """
        单参数PP图

        :param str column: 分析参数
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool boxcox: 是否进行box-cox变换
        :param float lmbda: box-cox变换的lmbda值
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def probplot_demo(column, start_date, end_date, boxcox, lmbda, save=False):
                print()

            interact_manual(probplot_demo,
                            column=widgets.Dropdown(options=columns, value=columns[0], description='参数: '),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            boxcox=widgets.Checkbox(value=False, description='是否进行box-cox变换', disabled=False),
                            lmbda=widgets.Text(value=None, description='lmbda值', disabled=False),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            单参数PP图')
        return interact_manual(self._probplot,
                               column=widgets.Dropdown(options=list(self.columns), value=self.columns[0],
                                                       description='参数: '),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               boxcox=widgets.Checkbox(value=False, description='是否进行box-cox变换', disabled=False),
                               lmbda=widgets.Text(value=None, description='lmbda值', disabled=False),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _scatterplot(self, column_1, column_2, start_date, end_date, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        scatterplot_df_1 = self.loc[(self.index >= start_date) & (self.index <= end_date)][column_1]
        scatterplot_df_2 = self.loc[(self.index >= start_date) & (self.index <= end_date)][column_2]
        set_figsize(10, 5)
        sns.scatterplot(x=scatterplot_df_1, y=scatterplot_df_2)
        if save:
            plt.savefig(f"参数{column_1}和{column_2}的散点图.png", dpi=600)

    def scatterplot(self):
        """
        双变量散点图

        :param str column_1: 分析参数1
        :param str column_2: 分析参数2
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def scatterplot_demo(column_1, column_2, start_date, end_date, save=False):
                print()

            interact_manual(scatterplot_demo,
                            column_1=widgets.Dropdown(options=columns, value=columns[0], description='X轴参数: '),
                            column_2=widgets.Dropdown(options=columns, value=columns[1], description='Y轴参数: '),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            双参数散点图')
        return interact_manual(self._scatterplot,
                               column_1=widgets.Dropdown(options=list(self.columns), value=self.columns[0],
                                                         description='X轴参数: '),
                               column_2=widgets.Dropdown(options=list(self.columns), value=self.columns[1],
                                                         description='Y轴参数: '),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _pairplot(self, pairplot_columns, start_date, end_date, save=False):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        pairplot_columns = list(pairplot_columns)
        pairplot_df = self.loc[(self.index >= start_date) & (self.index <= end_date)][pairplot_columns]
        set_figsize(10, 5)
        sns.pairplot(pairplot_df)
        if save:
            plt.savefig(f"参数{pairplot_columns}的两两关系图.png", dpi=600)

    def pairplot(self):
        """
        多参数的两两关系图

        :param list pairplot_columns: 分析参数列表
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def pairplot_demo(pairplot_columns, start_date, end_date, save=False):
                print()

            interact_manual(pairplot_demo,
                            pairplot_columns=widgets.SelectMultiple(options=columns, value=columns[0:2],
                                                                    description='多参数选择'),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像 ', disabled=False));
        """
        print('\n            多参数的两两关系图')
        return interact_manual(self._pairplot,
                               pairplot_columns=widgets.SelectMultiple(options=self.columns.tolist(),
                                                                       value=self.columns[0:2].tolist(),
                                                                       description='多参数选择'),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))

    def _heatmap(self, column, num, start_date, end_date, save=False):
        set_figsize(10, 5)
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        heatmap_df = self.loc[(self.index >= start_date) & (self.index <= end_date)]
        corr_largest = heatmap_df.corr().nlargest(num, column)[column]
        print(f"与参数{column}正相关性最强的{num}个参数:\n{corr_largest}")
        cols_largest = corr_largest.index
        sns.heatmap(heatmap_df[cols_largest].corr())
        if save:
            plt.savefig(f"与参数{column}正相关性最强的{num}个参数.png", dpi=600)
        corr_smallest = heatmap_df.corr().nsmallest(num, column)[column]
        print(f"与参数{column}负相关性最强的{num}个参数:\n{corr_smallest}")
        cols_smallest = corr_smallest.index
        sns.heatmap(heatmap_df[cols_smallest].corr())
        if save:
            plt.savefig(f"与参数{column}负相关性最强的{num}个参数.png", dpi=600)

    def heatmap(self):
        """
        相关性热点图

        :param str column: 分析参数
        :param int num: 展示与分析参数相关性最强的参数的数量
        :param str start_date: 开始日期
        :param str end_date: 结束日期
        :param bool save: 是否保存作图

        .. jupyter-execute::
            :hide-code:

            import ipywidgets as widgets
            from ipywidgets import interact_manual
            from datetime import datetime, timedelta
            interact_manual.opts['manual_name'] = '确认'

            columns = ['param_1', 'param_2', 'param_3', 'param_4']
            today = datetime.now()
            yesterday = datetime.now() - timedelta(1)

            def heatmap_demo(column, num, start_date, end_date, save=False):
                print()

            interact_manual(heatmap_demo,
                            column=widgets.Dropdown(options=columns, value=columns[0], description='参数: '),
                            num=widgets.IntSlider(value=10, min=1, max=50, step=1, description='数量', disabled=False),
                            start_date=widgets.DatePicker(value=yesterday, description='开始日期: '),
                            end_date=widgets.DatePicker(value=today, description='结束日期: '),
                            save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False));
        """
        print('\n            相关性热点图')
        return interact_manual(self._heatmap,
                               column=widgets.Dropdown(options=list(self.columns), value=self.columns[0],
                                                       description='参数: '),
                               num=widgets.IntSlider(value=10, min=1, max=50, step=1,
                                                     description='数量', disabled=False),
                               start_date=widgets.DatePicker(value=self.index[0], description='开始日期: '),
                               end_date=widgets.DatePicker(value=self.index[-1], description='结束日期: '),
                               save=widgets.Checkbox(value=False, description='是否保存图像', disabled=False))
