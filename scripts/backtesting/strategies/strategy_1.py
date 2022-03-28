import backtrader as bt

class SMA_ATR(bt.Strategy):
    def __init__(self): 
        """Simple moving average on (14, 21) periods and ATR Backtest on (14) period.
        
        If there is an SMA crossover indicating a buy or sell signal, the ATR should be above 70 to place a trade.
        The idea is that a trend reversal with a high volatility signifies a strong buying signal.
        
        order (obj): The order object that holds the status of a trade.
        trade_size (float): How much capital to allocate to a trade in USD.
        sma1 (int): A simple moving average of the last 14 candles.
        sma2 (int): A simple moving average of the last 21 candles.
        atr (int): A value indicating how much momentum there is in the past 14 candles.
        crossover (int): 0 for no crossover, 1 indicating uptrend reversal and -1 indicating downtrend reversal.
        
        """
        self.order = None
        self.trade_size = 0
        self.sma1 = bt.ind.SMA(period=14)
        self.sma2 = bt.ind.SMA(period=21)
        self.atr = bt.ind.ATR(period=14)
        self.crossover = bt.ind.CrossOver(self.sma1, self.sma2)
        
    def log(self, txt, dt=None):
        ''' Log closing prices'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return

        if order.status in [order.Completed]:
            if order.isbuy(): # BUY
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
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed: return
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