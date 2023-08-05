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
# Description : 数据传输
# Author : kanxiangyang

import ipywidgets as widgets
from ipywidgets import interact_manual
from IPython.core.interactiveshell import InteractiveShell
import pandas as pd
import boto3
import tarfile
import os
import mavis
from . import config

# 交互设置
interact_manual.opts['manual_name'] = '确认'
InteractiveShell.ast_node_interactivity = 'all'


def _set_config(aws_access_key_id, aws_secret_access_key):
    if not os.path.isdir('/root/.aws'):
        os.mkdir('/root/.aws')
    credentials = open('/root/.aws/credentials', 'w+')
    credentials.write(
        f"[default]\naws_access_key_id = {aws_access_key_id}\naws_secret_access_key = {aws_secret_access_key}")
    aws_config = open('/root/.aws/config', 'w+')
    aws_config.write(f"[default]\nregion = cn-northwest-1\noutput = json")
    print('AWS S3数据桶凭据设置成功')


def set_config():
    """
    设置AWS S3数据桶传输凭据

    :param str aws_access_key_id: 数据桶访问密钥ID
    :param str aws_secret_access_key: 数据桶访问密钥

    .. note::
        数据桶访问ID和访问密钥可以登录AWS账户获取，默认地区为cn-northwest-1

        https://console.amazonaws.cn/iam/home?region=cn-northwest-1#/security_credentials

        服务器中的设置保存在/root/.aws/config和/root/.aws/credentials中

    .. jupyter-execute::
        :hide-code:

        import ipywidgets as widgets
        from ipywidgets import interact_manual
        interact_manual.opts['manual_name'] = '确认'

        def set_config_demo(aws_access_key_id, aws_secret_access_key):
            print("演示成功")

        interact_manual(set_config_demo,
                        aws_access_key_id=widgets.Text(value='请输入访问密钥 ID', description='访问密钥ID', disabled=False),
                        aws_secret_access_key=widgets.Text(value='请输入访问密钥', description='访问密钥', disabled=False));
    """
    print("AWS S3数据桶安全凭证")
    print("https://console.amazonaws.cn/iam/home?region=cn-northwest-1#/security_credentials")
    return interact_manual(_set_config,
                           aws_access_key_id=widgets.Text(value='请输入访问密钥 ID', description='访问密钥ID', disabled=False),
                           aws_secret_access_key=widgets.Text(value='请输入访问密钥', description='访问密钥', disabled=False)
                           )


def _upload(filename, directory, compress=True):
    client = boto3.client('s3')
    if compress:
        tarfile_name = filename.split(".", 1)[0] + ".tar.gz"
        t = tarfile.open(tarfile_name, "w:gz")
        t.add(filename)
        t.close()
        print('压缩成功')
        tarfile_name = tarfile_name.split("/")[-1]
        client.upload_file(Filename=tarfile_name, Bucket=config.bucket_name,
                           Key=directory + "/" + tarfile_name)
        print('上传成功')
        os.remove(tarfile_name)
        print(f'保存路径:\n目录:{directory}\n文件:{tarfile_name}')
    else:
        client.upload_file(Filename=filename, Bucket=config.bucket_name, Key=directory + "/" + filename.split("/")[-1])
        filename = filename.split("/")[-1]
        print('上传成功')
        print(f'保存路径:\n目录:{directory}\n文件:{filename}')


def upload():
    """
    数据上传至AWS S3数据桶

    :param str filename: 要上传到数据桶的本地文件路径
    :param str directory: 上传到数据桶中的该目录下
    :param bool compress: 是否压缩文件，压缩格式为tar.gz

    .. note::
        本地文件路径可以是文件的绝对路径或者相对路径，上传目录不需要打斜杠'/'

    .. jupyter-execute::
        :hide-code:

        import ipywidgets as widgets
        from ipywidgets import interact_manual
        interact_manual.opts['manual_name'] = '确认'

        def upload_demo(filename, directory, compress=True):
            print()

        interact_manual(upload_demo,
                        filename=widgets.Text(value='请输入本地文件路径', description='本地文件名', disabled=False),
                        directory=widgets.Text(value='请指定上传文件所在文件夹名', description='上传目录', disabled=False),
                        compress=widgets.Checkbox(value=True, description='是否压缩', disabled=False));
    """
    return interact_manual(_upload,
                           filename=widgets.Text(value='请输入本地文件路径', description='本地文件名', disabled=False),
                           directory=widgets.Text(value='请指定上传文件所在文件夹名', description='上传目录', disabled=False),
                           compress=widgets.Checkbox(value=True, description='是否压缩', disabled=False))


def _download(directory, key, filename):
    filedir = os.path.dirname(filename)
    if not os.path.isdir(filedir) and filedir:
        os.makedirs(filedir, mode=0o777)
    boto3.client('s3').download_file(Bucket=config.bucket_name, Key=directory + "/" + key, Filename=filename)
    print('下载成功')
    if not filedir:
        filename = './' + filename
    print(f'保存路径为{filename}')


def download():
    """
    从AWS S3数据桶下载数据

    :param str directory: 下载目录
    :param str key: 下载文件名
    :param str filename: 保存文件名

    .. jupyter-execute::
        :hide-code:

        import ipywidgets as widgets
        from ipywidgets import interact_manual
        interact_manual.opts['manual_name'] = '确认'

        def download_demo(directory, key, filename):
            print()

        interact_manual(download_demo,
                        directory=widgets.Text(value='请输入下载文件所在文件夹名', description='下载目录', disabled=False),
                        key=widgets.Text(value='请输入下载文件名称', description='下载文件名', disabled=False),
                        filename=widgets.Text(value='请输入保存文件路径', description='保存文件名', disabled=False));

    """
    return interact_manual(_download,
                           directory=widgets.Text(value='请输入下载文件所在文件夹名', description='下载目录', disabled=False),
                           key=widgets.Text(value='请输入下载文件名称', description='下载文件名', disabled=False),
                           filename=widgets.Text(value='请输入保存文件路径', description='保存文件名', disabled=False))


def read(directory, key):
    """
    读取AWS S3数据桶上的数据

    :param str directory: 数据桶目录
    :param str key: 数据桶文件名
    :return: pandas.DataFrame

    """
    prefix = "/data/tmp/"
    filename = prefix + directory + "/" + key
    if not os.path.isdir(prefix + directory):
        os.makedirs(prefix + directory, mode=0o777)
    if not os.path.exists(filename):
        boto3.client("s3").download_file(Bucket=config.bucket_name, Key=directory + "/" + key, Filename=filename)
    if key.endswith("tar.gz"):
        t = tarfile.open(filename)
        t.extract(prefix + directory)
        os.remove(filename)
        filename = filename.rstrip("tar.gz")
    else:
        pass
    if filename.endswith('.csv'):
        data = pd.read_csv(filename, index_col=0, parse_dates=True).sort_index(axis=0, ascending=True)
    elif filename.endswith('.h5'):
        data = pd.read_hdf(filename).sort_index(axis=0, ascending=True)
    else:
        raise IOError('路径格式错误，请输入csv格式或h5格式')
    return data

