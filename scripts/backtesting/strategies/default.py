import backtrader as bt

class BuyAndHold(bt.Strategy):
    def __init__(self): 
        self.order = None
        self.epoch = 0
        self.dataset_length = len(self.data.close.array)
        self.starting_val = self.broker.getvalue()
    
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('[INFO]: {} {}'.format(dt.isoformat(), txt))
        
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]: return
        if order.status in [order.Completed]:
            if order.isbuy(): # BUY
                self.log('EXECUTED at Price: %.2f, Cost: %.2f, Comm %.2f\n' % (order.executed.price, order.executed.value, order.executed.comm))
                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('EXECUTED at Price: %.2f, Cost: %.2f, Comm %.2f\n' %(order.executed.price, order.executed.value, order.executed.comm))
            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected\n')
        self.order = None
        
    def notify_trade(self, trade):
        if not trade.isclosed: return
        date = self.datas[0].datetime.date(0)
        self.log('{} PROFIT/LOSS \nGROSS: {} \nNET: {} \n'.format(date, trade.pnl, trade.pnlcomm))
        
    def next(self):
        self.epoch += 1
        if self.order: return
        if not self.position and not(self.position and self.epoch == self.dataset_length):
            trade_amount = (0.5 * self.broker.cash)
            self.trade_size = trade_amount / self.data.close[0]
            self.order = self.buy(exectype=bt.Order.Market, price=self.data.close[0], size=self.trade_size)
            self.log('BUY ORDER ID: {}'.format(self.order.ref))
        elif self.position and self.epoch == self.dataset_length -1:
            self.order = self.sell(exectype=bt.Order.Market, price=self.data.close[0], size=self.trade_size)
            self.log('SELL ORDER ID: {}'.format(self.order.ref))
    
    def stop(self):
        roi = str(round((self.broker.getvalue() - self.starting_val)/self.starting_val * 100, 2))
        print('ROI: {}%'.format(roi))