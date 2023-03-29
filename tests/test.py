import requests

url = "https://east.albion-online-data.com/api/v2/stats/history/T4_BAG?time-scale=1"

response = requests.get(url)

print(response.content)
