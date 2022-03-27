from urllib import request, parse

data = parse.urlencode({ 'text': 'hello' }).encode()
req = request.Request("https://api.chanify.net/v1/sender/CICH9ZQGEiJBQk1ZQVBISzVNN1ZUM1FQWEdWNU0yRExaTUdHREpCM0VJIgIIAQ.duiScbglM5LKBCFQ8YaAQxc8R-hDRWsWpGVUgSSBRTg", data=data)
request.urlopen(req)