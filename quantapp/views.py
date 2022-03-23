from django.shortcuts import render
from datetime import datetime
from binance.client import Client

def home(request):
    context = {}
    test_key = 'wzxO0nmWGlU2HHfP5qWWnSdy5dsosGILc1ETF3nISswDVe5QEGSYq5fLa9hGXRwB'
    test_secret = 'VEx7sIWlKrw3dzmqL1K08PwrczLRNaVdiVCqwTZ7engb9gKvFZ9nZ3EMOKVzi37r'

    test_client = Client(test_key, test_secret)
    test_client.API_URL = 'https://testnet.binance.vision/api'
    account_details = test_client.get_account()
    context['client'] = 'Test Account'
    context['can_trade'] = account_details['canTrade']
    context['balances_info'] = account_details['balances']
    context['permissions'] = account_details['permissions']
    context['account_type'] = account_details['accountType']
    context['time_updated'] = datetime.fromtimestamp(account_details['updateTime']/1000).strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'index.html', context)