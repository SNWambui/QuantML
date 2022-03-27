import backtrader as bt
import vectorbt as vbt

class Broker(bt.observers.Broker):
    alias = ('Portfolio Value',)
    lines = ('value',)
    plotinfo = dict(plot=True, subplot=True)

    def next(self):
        # self.lines.cash[0] = self._owner.broker.getcash()
        self.lines.value[0] = value = self._owner.broker.getvalue()


class BuySellArrow(bt.observers.BuySell):
    plotlines = dict(
        buy=dict(marker='$\u21E7$', markersize=12.0),
        sell=dict(marker='$\u21E9$', markersize=12.0)
    )

class TestStrategy(bt.Strategy):
    def __init__(self): 
        self.order = None
        self.trade_size = 0
        self.sma1 = bt.ind.SMA(period=14)
        self.sma2 = bt.ind.SMA(period=21)
        self.atr = bt.ind.ATR(period=14)
        # self.rsi = bt.indicators.RelativeStrengthIndex()
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)
        
    def log(self, txt, dt=None):
        ''' Log closing prices'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f\n' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f\n' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected\n')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT - GROSS: %.2f NET: %.2f \n' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        if self.order:
            return

        if not self.position:
            if (self.crossover == 1 and self.atr > 70):
                trade_amount = (0.5 * self.broker.cash)
                self.trade_size = trade_amount / self.data.close[0]
                self.order = self.buy(exectype=bt.Order.Market, price=self.data.close[0], size=self.trade_size)
                self.log('BUY CREATE, %.2f' % self.data.close[0])         

        else:
            if (self.crossover == -1 and self.atr > 70):
                self.sell(exectype=bt.Order.Market, price=self.data.close[0], size=self.trade_size)
                self.log('SELL CREATE, %.2f' % self.data.close[0]) 
    
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
cerebro.addstrategy(TestStrategy)
cerebro.addobserver(BuySellArrow)
cerebro.addobserver(Broker)

#Run Cerebro Engine
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run(stdstats=False)
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()