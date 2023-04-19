import requests
import json

# 获取所有物品ID
item_ids = 'ITEMS_T1_FARM_CARROT_SEED'

# 查询所有城市、所有物品3小时内的物价情况
for item_id in item_ids:
    url = f'https://www.albion-online-data.com/api/v2/stats/history/{item_id}?locations=all&qualities=all&time-scale=3&date=2022-04-5'
    response = requests.get(url)
    data = response.json()
    print(json.dumps(data, indent=2))
