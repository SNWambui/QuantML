import vectorbt as vbt

start = '2022-01-01 UTC'
end = '2022-03-15 UTC'
closing_btc_prices = vbt.BinanceData.download('BTCUSDT', start=start, end=end, interval='1d').get('Close')
closing_btc_prices.plot()

rsi = vbt.RSI.run(closing_btc_prices)
entries = rsi.rsi_below(30)
exits = rsi.rsi_above(70)

portfolio = vbt.Portfolio.from_signals(closing_btc_prices, entries, exits, init_cash=10000)
print(portfolio.total_profit())
print(portfolio.sharpe_ratio())
print(portfolio.returns())
