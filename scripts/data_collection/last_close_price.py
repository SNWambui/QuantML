import schedule
import vectorbt as vbt
from datetime import datetime

# from binance.client import Client
# API_KEY = 'sI7t1YatbBiZLrZi6RdL4zShIzo0l0P3E4u6ZZlQwuYDR9ByrbLueHEYFTezWVIM'
# API_SECRET = 'sIk8ruShPbX8AEpu9ByRURjm1wDBVhb4ZTCZwfuD6qt5LTzIl97d5aZljhJPzqyA'
# client = Client(API_KEY, API_SECRET)

asset = 'BTCUSDT'
start = '5 minutes ago UTC'
end = 'now UTC'
interval = '1m'

# btc_data = vbt.BinanceData.download_symbol(
#     symbol=asset,
#     client=client,
#     interval=interval,
#     start=start,
#     end='now UTC',
#     show_progress=False
# )


def job(asset, interval, start, end):
    btc_data = vbt.BinanceData.download(
        symbols=asset, 
        start=start, 
        end=end, 
        interval=interval, 
        show_progress=False
    ).get()
    print("Asset: {} Time: {} Close: {} Close Time: {}".format(asset, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), btc_data.iloc[-2]['Close'], btc_data.iloc[-2]['Close time']))

schedule.every().minute.at(":00").do(job, asset, interval, start, end)
while True:
    schedule.run_pending()

