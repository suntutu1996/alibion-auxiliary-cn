import requests
import configparser
import os

# 获取config.ini的路径
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini'))

# 创建config对象并读取配置文件
config = configparser.ConfigParser()
config.read(config_path)

# 获取配置参数
api_url = config.get('dataConfig', 'api_url')

url = api_url + "v2/stats/history/T5_BAG@1?time-scale=1"

response = requests.get(url)

print(response.content)
