import time
from binance.client import Client

# Real account
API_KEY = 'sI7t1YatbBiZLrZi6RdL4zShIzo0l0P3E4u6ZZlQwuYDR9ByrbLueHEYFTezWVIM'
API_SECRET = 'sIk8ruShPbX8AEpu9ByRURjm1wDBVhb4ZTCZwfuD6qt5LTzIl97d5aZljhJPzqyA'
client = Client(API_KEY, API_SECRET)

while True:
    btc_info = client.get_symbol_ticker(symbol="BTCUSDT")
    print("Asset: {} Price: {}".format(btc_info['symbol'], btc_info['price']))
    time.sleep(1)