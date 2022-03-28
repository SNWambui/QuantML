def print_portfolio(results, trade_details):
    print("Net profit/loss: $", round(float(trade_details['pnl']['net']['total']), 2))
    print("Total trades: ", trade_details['total']['total'])
    print("Total trades won: " + str(trade_details['won']['total']) + " (+$" + str(round(float(trade_details['won']['pnl']['total']),2)) + ")")
    print("Total trades lost: " + str(trade_details['lost']['total']) + " (-$" + str(round(float(abs(trade_details['lost']['pnl']['total'])),2)) + ")")
    print("Open trades left: ", trade_details['total']['open'])
    print("Longest winning streak: ", trade_details['streak']['won']['longest'])
    print("Longest losing streak: ", trade_details['streak']['lost']['longest'])
    try:
        print("Win ratio: ", round(trade_details['won']['total']/trade_details['lost']['total'], 2))
    except ZeroDivisionError:
        if float(trade_details['streak']['won']['longest']) > 0:
            print("Win ratio: ", trade_details['streak']['won']['longest'])
        elif (float(trade_details['streak']['lost']['longest'])):
            print("Win ratio: ", trade_details['streak']['lost']['longest'])

    print("\n")
    print("Sharpe ratio: ", results[0].analyzers.sharpe.get_analysis()['sharperatio'])
    print("Annualized returns: ", round(results[0].analyzers.returns.get_analysis()['rnorm100'], 2), "%")
    print("Drawdown percentage: ", round(results[0].analyzers.drawdown.get_analysis()['max']['drawdown'], 2), "%")
    print("Max drawdown: $", round(results[0].analyzers.drawdown.get_analysis()['max']['moneydown'], 2))