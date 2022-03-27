import time
import requests

asset = 'BTCUSDT' 
key = "https://api.binance.com/api/v3/ticker/price?symbol={}".format(asset)

while True:
    data = requests.get(key)  
    data = data.json()
    print("{} price is {}".format(asset, data['price']))
    time.sleep(1)