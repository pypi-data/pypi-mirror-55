# coding=utf-8

import ccxt
import json

huobipro = ccxt.huobipro()
data = huobipro.fetch_ticker('BTC/USDT')

#print(data)

bid_huobi = data["info"]["bid"][0]
ask_huobi = data["info"]["ask"][0]

print("huobi",bid_huobi,ask_huobi)

binance = ccxt.binance()
#print(binance.fetch_ticker('BTC/USDT'))
bid_binance = float(data["info"]["bid"][0])
ask_binance = float(data["info"]["ask"][0])
print("binance",bid_binance,ask_binance)

okex = ccxt.okex()
#print(okex.fetch_ticker('BTC/USDT'))
data = okex.fetch_ticker('BTC/USDT')
bid_okex = data["info"]["buy"]
ask_okex = data["info"]["sell"]
print("okex",bid_okex,ask_okex)

#print(binance.load_markets())
#print(okex.load_markets())
print(huobipro.load_markets())

# hitbtc   = ccxt.hitbtc({'verbose': True})
# bitmex   = ccxt.bitmex()
# huobipro = ccxt.huobipro()
# exmo     = ccxt.exmo({
#     'apiKey': 'YOUR_PUBLIC_API_KEY',
#     'secret': 'YOUR_SECRET_PRIVATE_KEY',
# })
# kraken = ccxt.kraken({
#     'apiKey': 'YOUR_PUBLIC_API_KEY',
#     'secret': 'YOUR_SECRET_PRIVATE_KEY',
# })

# exchange_id = 'binance'
# exchange_class = getattr(ccxt, exchange_id)
# exchange = exchange_class({
#     'apiKey': 'YOUR_API_KEY',
#     'secret': 'YOUR_SECRET',
#     'timeout': 30000,
#     'enableRateLimit': True,
# })

# hitbtc_markets = hitbtc.load_markets()

# print(hitbtc.id, hitbtc_markets)
# print(bitmex.id, bitmex.load_markets())
# print(huobipro.id, huobipro.load_markets())

# print(hitbtc.fetch_order_book(hitbtc.symbols[0]))
# print(bitmex.fetch_ticker('BTC/USD'))
# print(huobipro.fetch_trades('LTC/CNY'))

# print(exmo.fetch_balance())

# # sell one ฿ for market price and receive $ right now
# print(exmo.id, exmo.create_market_sell_order('BTC/USD', 1))

# # limit buy BTC/EUR, you pay €2500 and receive ฿1  when the order is closed
# print(exmo.id, exmo.create_limit_buy_order('BTC/EUR', 1, 2500.00))

# # pass/redefine custom exchange-specific order params: type, amount, price, flags, etc...
# kraken.create_market_buy_order('BTC/USD', 1, {'trading_agreement': 'agree'})