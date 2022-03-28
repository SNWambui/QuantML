import backtrader as bt

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