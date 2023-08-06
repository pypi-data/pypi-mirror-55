# coding=utf-8

import multiprocessing
from time import sleep
from datetime import datetime, time

from vnpy.ConfigProduce.ClientQuickQuery import *

def get_chazhi( d1 , d2):
	r1 = 0.0
	r2 = 0.0
	r3 = 0.0
	r4 = 0.0
	if d1 and d2:
		#print(d1)
		#print(d2)
		bid1 = d1["bids"][0][0]
		ask1 = d1["asks"][0][0]

		bid2 = d2["bids"][0][0]
		ask2 = d2["asks"][0][0]

		try:
			r1 = (bid1 - ask2) / bid1
			r2 = (bid2 - ask1) / bid2

			r3 = (bid1 - bid2) / bid1
			r4 = (ask1 - ask2) / ask1
		except Exception,ex:
			pass
	return ( r1 , r2 , r3 , r4)

def test():
	s1 = ClientPosPriceQuery.QueryAllBinanceExchangeInfo()
	s2 = ClientPosPriceQuery.QueryAllHuobiExchangeInfo()

	#aa = list(set(s1.keys() + s2.keys()))
	aa = [ x for x in s1.keys() if x in s2.keys()]

	for key in aa:
		d1 = ClientPosPriceQuery.QueryOrderbook(key , EXCHANGE_BINANCE )
		d2 = ClientPosPriceQuery.QueryOrderbook(key , EXCHANGE_HUOBI )

		(r1 , r2 , r3 , r4) = get_chazhi(d1, d2)
		#print( key, r1, r2 , r3, r4)

		if r1 > 0.003 or r2 > 0.003:
			print( "important" , key , r1 , r2 , r3 , r4) 


if __name__ == "__main__":
	#s = ClientPosPriceQuery.QueryAllBinanceExchangeInfo()
	#print(s.keys())

	#u = ClientPosPriceQuery.QueryOrderbook("xrp_usdt" ,EXCHANGE_BINANCE )
	#print(u)

	test()
