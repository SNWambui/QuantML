import backtrader as bt
import vectorbt as vbt
import backtrader.analyzers as btanalyzers
from displays import print_portfolio
from strategies.default import BuyAndHold
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
cerebro.addstrategy(BuyAndHold)
cerebro.addobserver(BuySellArrow)
cerebro.addobserver(Broker)
cerebro.addanalyzer(btanalyzers.SharpeRatio, riskfreerate=0.0, _name = "sharpe")
cerebro.addanalyzer(btanalyzers.Transactions, _name = "trans")
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name = "trades")
cerebro.addanalyzer(btanalyzers.Returns, _name = "returns")
cerebro.addanalyzer(btanalyzers.DrawDown, _name = "drawdown")

#Run Cerebro Engine
print('\nStarting Portfolio Value: %.2f' % cerebro.broker.getvalue())
results = cerebro.run(stdstats=False)
trade_details = results[0].analyzers.trades.get_analysis()
print_portfolio(results, trade_details)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
# cerebro.plot()