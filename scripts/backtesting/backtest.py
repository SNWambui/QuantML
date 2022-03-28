import backtrader as bt
import vectorbt as vbt
from strategies.strategy_1 import SMA_ATR
from observers import Broker, BuySellArrow

# Get asset's historical data
btc_data = vbt.BinanceData.download(
    symbols='BTCUSDT', 
    start='10 days ago UTC', 
    end='1 minutes ago UTC', 
    interval='5m', 
    show_progress=False).get()

data = bt.feeds.PandasData(dataname=btc_data)

#Instantiate Cerebro engine
cerebro = bt.Cerebro()
cerebro.broker.setcash(100.0)
cerebro.broker.setcommission(commission=0.001) 
cerebro.broker.set_slippage_perc(0.005)

# Add the data and strategy
cerebro.adddata(data)
cerebro.addstrategy(SMA_ATR)
cerebro.addobserver(BuySellArrow)
cerebro.addobserver(Broker)

#Run Cerebro Engine
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run(stdstats=False)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()