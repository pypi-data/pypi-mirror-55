# 数据预览库
preview_repository = {
    '数据统计量': 'summary',
    '参数缺失值比例图': 'naplot',
    '单参数趋势图': 'timeplot',
    '单参数分布图': 'distplot',
    '单参数PP图': 'probplot',
    '双参数散点图': 'scatterplot',
    '多参数关系图': 'pairplot',
    '多参数相关性热点图': 'heatmap'
}

# 算法库
model_repository = {
    'DEMO演示算法': 'ModelDemo',
    '锅炉生产参数预测的神经网络算法': 'Boiler',
    '锅炉异常检测算法': 'IForest'

}

# 平台库
platform_repository = {
    '康普斯': 'kps',
    '瑞升华': 'sunevap',
    '精旺': 'jingwang',
    '先创': 'xianchuang',
    '方块': 'fangkuai',
    '济柴': 'emiot',
    '演示': 'demo'
}


# Mixiot接口
class API(object):
    def __init__(self, platform):
        self.platform = platform

    def apix_url(self):
        if self.platform == 'emiot':
            return "http://emiot.cnpc.com.cn:8008/pro/equipment/public_get_mosaic_by_key"
        else:
            return f"http://pro.{self.platform}.mixiot.top/v1/apix/mosaicByKey"

    def apiq_login_url(self):
        if self.platform == 'emiot':
            return "http://emiot.cnpc.com.cn:8009/api/login"
        else:
            return f"http://admin.{self.platform}.mixiot.top/api/login"

    def apiq_info_url(self):
        if self.platform == 'emiot':
            return "http://emiot.cnpc.com.cn:8009/api/equipment/menu_list"
        else:
            return f"http://admin.{self.platform}.mixiot.top/api/equipment/get_menu_list"

    def apiq_pro_url(self):
        if self.platform == 'emiot':
            return f"http://emiot.cnpc.com.cn:8009/api/pro/getMapping"
        else:
            return f"http://admin.{self.platform}.mixiot.top/api/pro/getMapping"

    def influx_export_url(self):
        if self.platform == 'emiot':
            return f"http://emiot.cnpc.com.cn:9009/export/export_data"
        else:
            return f"http://{self.platform}.mixiot.top:9009/export/export_data"


# 数据重采样方法
resample_method = \
    {
        '降采样取最新一条数据': 'first',
        '降采样取最早一条数据': 'last',
        '降采样取均值': 'mean',
        '降采样取求和': 'sum',
        '升采样取最近一条数据': 'nearest',
        '升采样取前一条数据': 'ffill',
        '升采样取后一条数据': 'bfill'
    }

# Mixiot S3数据桶
bucket_name = 'mixiot'
aws_access_key_id = "AKIATL43NOIHFVTCHE5T"
aws_secret_access_key = "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"