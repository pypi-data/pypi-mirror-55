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
# Description : Mixiot 数据查询
# Author : kanxiangyang

import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import HTML, display, FileLink
import pandas as pd
import requests
import time
import json
import os
import base64
from ast import literal_eval
from datetime import datetime, timedelta
from . import config

interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


def get_token(url, username, password):
    login_param = {'username': username, 'password': password, 'system': 'MixPro'}
    login_result = json.loads(requests.post(url=url, data=login_param).text)
    if login_result['code'] != 200:
        print(login_result['msg'])
        raise Exception
    if 'data' in list(login_result.keys()):
        token = login_result["data"]["token"]
    elif 'result' in list(login_result.keys()):
        token = login_result["result"]["token"]
    else:
        raise Exception
    return {'Authorization': 'Bearer ' + token}


def get_menu_list(url, headers):
    parameter = {"is_all": 1, "page_index": 1, "page_size": 20, "condition": ""}
    receive_data = json.loads(requests.post(url=url, headers=headers, data=parameter).text)
    if receive_data['code'] != 200:
        print("获取设备信息失败")
        raise Exception
    if 'data' in list(receive_data.keys()):
        result = receive_data['data']
    else:
        result = receive_data["result"]["data"]
    if not result:
        print("获取设备信息为空")
        raise Exception
    result = pd.DataFrame(result)
    result.index = result['equipment_id']
    result = result.drop(columns=['equipment_id']).sort_index(ascending=True)
    return result


def get_mapping(url, headers, equipment_id):
    parameter = {"equipment_id": equipment_id}
    receive_data = json.loads(requests.post(url=url, headers=headers, data=parameter).text)
    if receive_data['code'] != 200:
        print("获取mapping数据失败")
        raise Exception
    result = receive_data['result']['script']
    if not result:
        print("获取mapping数据为空")
        raise Exception
    result = pd.Series({i[0]: i[-1] for i in result})
    return result


def get_data(url, headers, equipment_id, start_time, end_time, page_size, keys):
    start_time = pd.to_datetime(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time = pd.to_datetime(end_time).strftime('%Y-%m-%d %H:%M:%S')
    keys = str(list(keys)).replace("'", '"')
    parameter = {'equipment_id': equipment_id, 'page_size': page_size, 'page_index': '1',
                 'end_time': end_time, 'start_time': start_time, 'keys': keys}
    receive_data = json.loads(requests.post(url=url, headers=headers, data=parameter).text)
    if receive_data['code'] != 200:
        print("获取fidis数据失败")
    else:
        result = receive_data["result"]["data"]
        if not result:
            print("获取fidis数据为空")
        time_index = pd.to_datetime([j['time'] for j in result])
        df = pd.DataFrame([j['value'] for j in result], index=time_index).sort_index(ascending=True)
        return df


def export_data(url, headers, equipment_id, start_time, end_time, keys, h5, merge, resample, method):
    start_time = pd.to_datetime(start_time).strftime('%Y-%m-%d %H:%M:%S')
    end_time = pd.to_datetime(end_time).strftime('%Y-%m-%d %H:%M:%S')
    keys = str(list(keys))
    parameter = {'equipment_id': equipment_id, 'start_time': start_time, 'end_time': end_time, 'keys': keys,
                 'h5': h5, 'merge': merge, 'resample': resample, 'method': method}
    receive_data = json.loads(requests.post(url=url, headers=headers, data=parameter).text)
    if receive_data['code'] != 200:
        print("导出数据失败")
        print(receive_data)
        raise Exception
    else:
        status_id = receive_data['result']['state']
        status_url = url.split("/export/export_data")[0] + f"/status/{status_id}"
        download_url = url.split("/export/export_data")[0] + f"/download/{status_id}"
        print(f'请等待后台任务完成，当前任务ID为{status_id}')
        count = 0
        while True:
            time.sleep(10)
            receive_data = json.loads(requests.get(url=status_url).text)
            if receive_data['code'] != 200:
                break
            elif receive_data['result']['state'] == 'FAILURE':
                print("后台任务失败")
                break
            elif receive_data['result']['state'] == 'SUCCESS':
                print("后台任务成功")
                break
            else:
                count += 1
                print(f"任务进行中...{count * 10}秒")
    return HTML(f'<a href="{download_url}">下载数据</a>')


def create_download_link(df, title="Download CSV file", filename="data.csv"):
    csv = df.to_csv(encoding='utf_8_sig')
    b64 = base64.b64encode(csv.encode('utf_8_sig'))
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload, title=title, filename=filename)
    return HTML(html)


class Mixiot(object):
    def __init__(self):
        self.platform_en = None
        self.equipment_id = None
        self.headers = None
        self.equipment_info = None
        self.mapping_info = None

    def live_plot(self, keys, interval):
        if 'status_code' in self.equipment_info.columns:
            if self.equipment_info.loc[self.equipment_id, 'status_code'] != 1:
                status_name = self.equipment_info.loc[self.equipment_id, 'status_name']
                print(f"警告: 设备当前状态为{status_name}")
        interval = literal_eval(interval)
        keys = [self.mapping_info[self.mapping_info == key].index[0] for key in keys]
        apix_url = config.API(platform=self.platform_en).apix_url()
        live_result = pd.DataFrame()
        while True:
            time_now = datetime.now()
            start_time = (time_now - timedelta(seconds=interval)).strftime('%Y-%m-%d %H:%M:%S')
            end_time = time_now.strftime('%Y-%m-%d %H:%M:%S')
            page_size = 10
            result = get_data(url=apix_url, headers=self.headers, equipment_id=self.equipment_id, start_time=start_time,
                              end_time=end_time, page_size=page_size, keys=keys)
            live_result.append(result)
            print(live_result)
            delta_seconds = (datetime.now() - time_now).seconds
            time.sleep(interval - delta_seconds)

    def select_mosaic(self, start_time, end_time, page_size, keys, cn=True, save=False):
        keys = [self.mapping_info[self.mapping_info == key].index[0] for key in keys]
        apix_url = config.API(platform=self.platform_en).apix_url()
        result = get_data(url=apix_url, headers=self.headers, equipment_id=self.equipment_id, start_time=start_time,
                          end_time=end_time, page_size=page_size, keys=keys)
        if 'status_code' in self.equipment_info.columns:
            if self.equipment_info.loc[self.equipment_id, 'status_code'] != 1:
                status_name = self.equipment_info.loc[self.equipment_id, 'status_name']
                print(f"警告: 设备当前状态为{status_name}")
        if cn:
            result.columns = self.mapping_info[result.columns]
        start_time = pd.to_datetime(start_time).strftime('%Y-%m-%d-%H-%M-%S')
        end_time = pd.to_datetime(end_time).strftime('%Y-%m-%d-%H-%M-%S')
        filename = f"{self.platform_en}_device{self.equipment_id}_{start_time}_{end_time}.csv"
        if not os.path.isdir("/data/tmp"):
            os.makedirs("/data/tmp", mode=0o777)
        result.to_csv(f"/data/tmp/{filename}", encoding='utf_8_sig')
        if save:
            display(FileLink(f"/data/tmp/{filename}"))
            return create_download_link(result, title="下载数据到本地", filename=filename)
        else:
            display(FileLink(f"/data/tmp/{filename}"))
            return result

    def select_device(self, equipment_name):
        self.equipment_id = self.equipment_info[self.equipment_info['equipment_name'] == equipment_name].index[0]
        apiq_pro_url = config.API(platform=self.platform_en).apiq_pro_url()
        self.mapping_info = get_mapping(url=apiq_pro_url, headers=self.headers, equipment_id=self.equipment_id)
        key_list = self.mapping_info.values.tolist()
        default_start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        default_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return interact_manual(self.select_mosaic,
                               keys=widgets.SelectMultiple(options=key_list,
                                                           value=key_list[:2],
                                                           description='设备参数'),
                               start_time=widgets.Text(value=default_start_time, description='开始时间', disabled=False),
                               end_time=widgets.Text(value=default_end_time, description='结束时间', disabled=False),
                               page_size=widgets.Text(value='100', description='请求条数', disabled=False),
                               cn=widgets.Checkbox(value=False, description='是否返回中文参数', disabled=False),
                               save=widgets.Checkbox(value=False, description='是否保存数据', disabled=False)
                               )

    def login(self, username, password):
        login_url = config.API(platform=self.platform_en).apiq_login_url()
        self.headers = get_token(url=login_url, username=username, password=password)
        apiq_info_url = config.API(platform=self.platform_en).apiq_info_url()
        self.equipment_info = get_menu_list(url=apiq_info_url, headers=self.headers)
        equipment_name_list = self.equipment_info['equipment_name'].values.tolist()
        return interact(self.select_device,
                        equipment_name=widgets.Dropdown(options=equipment_name_list,
                                                        value=equipment_name_list[0],
                                                        description='设备 '))

    def select_platform(self, platform_cn):
        self.platform_en = config.platform_repository[platform_cn]
        return interact_manual(self.login,
                               username=widgets.Text(value='admin', description='用户名', disabled=False),
                               password=widgets.Text(value='', description='密码', disabled=False)
                               )

    def __call__(self):
        return interact(self.select_platform,
                        platform_cn=widgets.Dropdown(options=list(config.platform_repository.keys()),
                                                     value=list(config.platform_repository.keys())[0],
                                                     description='MIXIOT 平台 '))


class Export(object):
    def __init__(self):
        self.platform_en = None
        self.equipment_id = None
        self.headers = None
        self.equipment_info = None
        self.mapping_info = None

    def select_mosaic(self, start_time, end_time, keys, h5, merge, resample, method):
        keys = [self.mapping_info[self.mapping_info == key].index[0] for key in keys]
        influx_export_url = config.API(platform=self.platform_en).influx_export_url()
        if resample and method:
            resample = config.resample_method[resample]
        else:
            resample = ""
            method = ""
        if 'status_code' in self.equipment_info.columns:
            if self.equipment_info.loc[self.equipment_id, 'status_code'] != 1:
                status_name = self.equipment_info.loc[self.equipment_id, 'status_name']
                print(f"警告: 设备当前状态为{status_name}")
        return export_data(url=influx_export_url, headers=self.headers, equipment_id=self.equipment_id,
                           start_time=start_time, end_time=end_time, keys=keys, h5=h5, merge=merge, resample=resample,
                           method=method)

    def select_device(self, equipment_name):
        self.equipment_id = self.equipment_info[self.equipment_info['equipment_name'] == equipment_name].index[0]
        apiq_pro_url = config.API(platform=self.platform_en).apiq_pro_url()
        self.mapping_info = get_mapping(url=apiq_pro_url, headers=self.headers, equipment_id=self.equipment_id)
        key_list = self.mapping_info.values.tolist()
        default_start_time = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        default_end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return interact_manual(self.select_mosaic,
                               keys=widgets.SelectMultiple(options=key_list,
                                                           value=key_list[:2],
                                                           description='设备参数'),
                               start_time=widgets.Text(value=default_start_time, description='开始时间', disabled=False),
                               end_time=widgets.Text(value=default_end_time, description='结束时间', disabled=False),
                               h5=widgets.Checkbox(value=False, description='是否保存为h5', disabled=False),
                               merge=widgets.Checkbox(value=True, description='是否合并', disabled=False),
                               resample=widgets.Text(value=None, description='重采样时间间隔/秒', disabled=False),
                               method=widgets.Dropdown(options=list(config.resample_method.keys()), value=None,
                                                       description='重采样方法', disabled=False)
                               )

    def login(self, username, password):
        login_url = config.API(platform=self.platform_en).apiq_login_url()
        self.headers = get_token(url=login_url, username=username, password=password)
        apiq_info_url = config.API(platform=self.platform_en).apiq_info_url()
        self.equipment_info = get_menu_list(url=apiq_info_url, headers=self.headers)
        equipment_name_list = self.equipment_info['equipment_name'].values.tolist()
        return interact(self.select_device,
                        equipment_name=widgets.Dropdown(options=equipment_name_list,
                                                        value=equipment_name_list[0],
                                                        description='设备 '))

    def select_platform(self, platform_cn):
        self.platform_en = config.platform_repository[platform_cn]
        return interact_manual(self.login,
                               username=widgets.Text(value='admin', description='用户名', disabled=False),
                               password=widgets.Text(value='', description='密码', disabled=False)
                               )

    def __call__(self):
        return interact(self.select_platform,
                        platform_cn=widgets.Dropdown(options=list(config.platform_repository.keys()),
                                                     value=list(config.platform_repository.keys())[0],
                                                     description='MIXIOT 平台 '))


class Mapping(object):
    def __init__(self):
        self.platform_en = None
        self.equipment_id = None
        self.headers = None
        self.equipment_info = None
        self.mapping_info = None

    def select_device(self, equipment_name, save):
        self.equipment_id = self.equipment_info[self.equipment_info['equipment_name'] == equipment_name].index[0]
        apiq_pro_url = config.API(platform=self.platform_en).apiq_pro_url()
        result = get_mapping(url=apiq_pro_url, headers=self.headers, equipment_id=self.equipment_id)
        result_df = pd.DataFrame(result, columns=['参数中文'])
        result_df.index.name = '参数ID'
        if save:
            filename = f"{self.platform_en}_{self.equipment_id}_mapping.csv"
            return create_download_link(result_df, title="下载数据到本地", filename=filename)
        else:
            return result_df

    def login(self, username, password):
        login_url = config.API(platform=self.platform_en).apiq_login_url()
        self.headers = get_token(url=login_url, username=username, password=password)
        apiq_info_url = config.API(platform=self.platform_en).apiq_info_url()
        self.equipment_info = get_menu_list(url=apiq_info_url, headers=self.headers)
        equipment_name_list = self.equipment_info['equipment_name'].values.tolist()
        return interact_manual(self.select_device,
                               equipment_name=widgets.Dropdown(options=equipment_name_list,
                                                               value=equipment_name_list[0],
                                                               description='设备 '),
                               save=widgets.Checkbox(value=False, description='是否保存', disabled=False))

    def select_platform(self, platform_cn):
        self.platform_en = config.platform_repository[platform_cn]
        return interact_manual(self.login,
                               username=widgets.Text(value='admin', description='用户名', disabled=False),
                               password=widgets.Text(value='', description='密码', disabled=False)
                               )

    def __call__(self):
        return interact(self.select_platform,
                        platform_cn=widgets.Dropdown(options=list(config.platform_repository.keys()),
                                                     value=list(config.platform_repository.keys())[0],
                                                     description='MIXIOT 平台 '))
