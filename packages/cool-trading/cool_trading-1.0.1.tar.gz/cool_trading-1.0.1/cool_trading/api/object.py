# coding=utf-8

from constant import EMPTY_STRING , EMPTY_INT , EMPTY_FLOAT, EMPTY_UNICODE , MAX_PRICE_NUM
from constant import Direction, Exchange, Interval, Offset, Status, Product, OptionType, OrderType

import time
from logging import INFO

class TickData(object):
    """
    Tick data contains information about:
        * last trade in market
        * orderbook snapshot
        * intraday market statistics.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        # 代码相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.vt_symbol = EMPTY_STRING            # 合约在vt系统中的唯一代码，通常是 合约代码.交易所代码

        self.name = EMPTY_STRING                # 合约名字
        self.gateway_name = EMPTY_STRING        # 网关名
        
        # 成交数据
        self.last_price = EMPTY_FLOAT            # 最新成交价
        self.last_volume = EMPTY_INT             # 最新成交量
        self.volume = EMPTY_INT                 # 今天总成交量
        self.open_interest = EMPTY_INT           # 持仓量
        self.time = EMPTY_STRING                # 时间 11:20:56.5
        self.date = EMPTY_STRING                # 日期 20151009
        self.datetime = None                    # python的datetime时间对象
        
        # 常规行情
        self.open_price = EMPTY_FLOAT            # 今日开盘价
        self.high_price = EMPTY_FLOAT            # 今日最高价
        self.low_price = EMPTY_FLOAT             # 今日最低价
        self.pre_close_price = EMPTY_FLOAT
        
        self.upperLimit = EMPTY_FLOAT           # 涨停价
        self.lowerLimit = EMPTY_FLOAT           # 跌停价
        
        # 五档行情
        self.bid_prices = [0.0] * MAX_PRICE_NUM
        self.ask_prices = [0.0] * MAX_PRICE_NUM

        self.bid_volumes = [0.0] * MAX_PRICE_NUM
        self.ask_volumes = [0.0] * MAX_PRICE_NUM


class BarData():
    """
    Candlestick bar data of a certain trading period.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self.vt_symbol = EMPTY_STRING        # vt系统代码
        self.symbol = EMPTY_STRING          # 代码
        self.exchange = EMPTY_STRING        # 交易所
    
        self.open = EMPTY_FLOAT             # OHLC
        self.high = EMPTY_FLOAT
        self.low = EMPTY_FLOAT
        self.close = EMPTY_FLOAT
        
        self.date = EMPTY_STRING            # bar开始的时间，日期
        self.time = EMPTY_STRING            # 时间
        self.datetime = None                # python的datetime时间对象
        
        self.volume = EMPTY_INT             # 成交量
        self.open_interest = EMPTY_INT       # 持仓量

        self.interval = None                # 时间周期    


class OrderData(object):
    """
    Order data contains information for tracking lastest status
    of a specific order.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        super(VtOrderData, self).__init__()
        
        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.vt_symbol = EMPTY_STRING            # 合约在vt系统中的唯一代码，通常是 合约代码.交易所代码
        
        self.orderid = EMPTY_STRING             # 订单编号
        self.vt_orderid = EMPTY_STRING           # 订单在vt系统中的唯一编号，通常是 Gateway名.订单编号
        
        # 报单相关
        self.direction = EMPTY_UNICODE          # 报单方向
        self.offset = EMPTY_UNICODE             # 报单开平仓
        self.price = EMPTY_FLOAT                # 报单价格
        self.totalVolume = EMPTY_INT            # 报单总数量
        self.tradedVolume = EMPTY_INT           # 报单成交数量
        self.status = EMPTY_UNICODE             # 报单状态
        
        self.order_time = EMPTY_STRING           # 发单时间
        self.cancelTime = EMPTY_STRING          # 撤单时间


class TradeData(object):
    """
    Trade data contains information of a fill of an order. One order
    can have several trade fills.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.vt_symbol = EMPTY_STRING            # 合约在vt系统中的唯一代码，通常是 合约代码.交易所代码
        
        self.tradeid = EMPTY_STRING             # 成交编号
        self.vt_tradeid = EMPTY_STRING           # 成交在vt系统中的唯一编号，通常是 Gateway名.成交编号
        
        self.orderid = EMPTY_STRING             # 订单编号
        self.vt_orderid = EMPTY_STRING           # 订单在vt系统中的唯一编号，通常是 Gateway名.订单编号
        
        # 成交相关
        self.direction = EMPTY_UNICODE          # 成交方向
        self.offset = EMPTY_UNICODE             # 成交开平仓
        self.price = EMPTY_FLOAT                # 成交价格
        self.volume = EMPTY_INT                 # 成交数量
        self.tradeTime = EMPTY_STRING           # 成交时间



class PositionData(object):
    """
    Positon data is used for tracking each individual position holding.
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        # 代码编号相关
        self.symbol = EMPTY_STRING              # 合约代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.vt_symbol = EMPTY_STRING            # 合约在vt系统中的唯一代码，合约代码.交易所代码  
        
        # 持仓相关
        self.direction = EMPTY_STRING           # 持仓方向
        self.position = EMPTY_INT               # 持仓量
        self.frozen = EMPTY_INT                 # 冻结数量
        self.price = EMPTY_FLOAT                # 持仓均价
        self.vt_positionid = EMPTY_STRING       # 持仓在vt系统中的唯一代码，通常是vtSymbol.方向
        self.yd_volume = EMPTY_FLOAT            # 昨持仓
        self.pnl = EMPTY_FLOAT                  # 持仓盈亏



class AccountData(object):
    """
    Account data contains information about balance, frozen and
    available.
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        # 账号代码相关
        self.accountid = EMPTY_STRING           # 账户代码
        self.vt_accountid = EMPTY_STRING         # 账户在vt中的唯一代码，通常是 Gateway名.账户代码
        
        # 数值相关
        self.balance = EMPTY_FLOAT              # 账户净值
        self.frozen = EMPTY_FLOAT               # 冻结金额
        self.available = EMPTY_FLOAT            # 可用资金


class LogData(object):
    """
    Log data is used for recording log messages on GUI or in log files.
    """

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self.time = time.strftime('%X', time.localtime())       # 日志生成时间
        self.msg = EMPTY_UNICODE                                # 日志信息
        self.level = INFO                                       # 日志级别
        self.gateway_name = EMPTY_STRING                        # gateway


class ContractData(object):
    """
    Contract data contains basic information about each contract traded.
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING              # 代码
        self.exchange = EMPTY_STRING            # 交易所代码
        self.vt_symbol = EMPTY_STRING           # 合约在vt系统中的唯一代码，通常是 合约代码.交易所代码
        self.name = EMPTY_UNICODE               # 合约中文名
        
        self.size = EMPTY_INT                   # 合约大小
        self.pricetick = EMPTY_FLOAT            # 合约最小价格TICK

        self.min_volume = 1                     # 最小交易数量
        self.stop_supported = False             # 是否支持stop order
        self.net_position = False               # 是否是净持仓
        self.history_data = False               # 是否支持历时K线数据

        self.option_strike = EMPTY_FLOAT        # 
        self.option_underlying = EMPTY_FLOAT    # vt_symbol of underlying contract
        self.option_type = None                 #
        self.option_expiry = None               # 

        

class SubscribeRequest(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING              # 代码
        self.exchange = EMPTY_STRING            # 交易所

        self.vt_symbol = EMPTY_STRING



class OrderRequest(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING              # 代码
        self.exchange = EMPTY_STRING            # 交易所
        self.vt_symbol = EMPTY_STRING           # VT合约代码

        self.price = EMPTY_FLOAT                # 价格
        self.volume = EMPTY_INT                 # 数量
    
        self.type = EMPTY_STRING                # 价格类型
        self.direction = EMPTY_STRING           # 买卖
        self.offset = EMPTY_STRING              # 开平
        


class CancelRequest:
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.symbol = EMPTY_STRING              # 代码
        self.exchange = EMPTY_STRING            # 交易所
        self.vt_symbol = EMPTY_STRING           # VT合约代码

        self.orderid = EMPTY_STRING             # 报单号



