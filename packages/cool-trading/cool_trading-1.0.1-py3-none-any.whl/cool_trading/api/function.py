# coding=utf-8


'''
	etc_btc  --> etcbtc
	eth_usdt.GATEWAY --> ethusdt
	ETH_USDT.GATEWAY --> ethusdt
'''
def getNoUnderLowerSymbol(symbol):
	return (symbol.split('.'))[0].replace('_','').lower()

'''
	ethusdt --> eth_usdt
	etcbtc  --> etc_btc
	ethusdt.HUOBI --> eth_usdt
	etcbtc.HUOBI  --> etc_btc
'''
def getFormatLowerSymbol(symbol):
	symbol = symbol.replace('_','')
	symbol = ((symbol.split('.'))[0]).lower()
	if 'usdt' in symbol:
		return symbol[:-4] + "_usdt"
	else:
		return symbol[:-3] + "_" + symbol[-3:]


if __name__ == "__main__":
	print(getNoUnderLowerSymbol("btc_usdt.HUOBI"))