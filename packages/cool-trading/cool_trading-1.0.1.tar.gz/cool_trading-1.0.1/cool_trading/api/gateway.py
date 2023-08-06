# coding=utf-8

import redis
import pika

from object import LogData

import cool_trading.config as config
from cool_trading.service import MQSender

from event import (
    EVENT_TICK,
    EVENT_ORDER,
    EVENT_TRADE,
    EVENT_POSITION,
    EVENT_ACCOUNT,
    EVENT_CONTRACT,
    EVENT_LOG,

    Event
)

class BaseGateway(object):
	# Fields required in setting dict for connect function.
    default_setting = {}

    # Exchanges supported in the gateway.
    exchanges = []

    def __init__(self, event_engine , gateway_name ):
        """"""
        self.event_engine = event_engine
        self.gateway_name = gateway_name

    def on_event(self, type , data = None):
        """
        General event push.
        """
        event = Event(type, data)
        self.event_engine.put(event)

    def on_tick(self, tick ):
        """
        Tick event push.
        Tick event of a specific vt_symbol is also pushed.
        """
        print("base on_tick")
        self.on_event(EVENT_TICK, tick)
        self.on_event(EVENT_TICK + tick.vt_symbol, tick)

    def on_rest_tick(self,tick):
        print("base on_rest_tick")
        self.on_event(EVENT_TICK, tick)
        self.on_event(EVENT_TICK + tick.vt_symbol, tick)

    def on_trade(self, trade):
        """
        Trade event push.
        Trade event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_TRADE, trade)
        self.on_event(EVENT_TRADE + trade.vt_symbol, trade)

    def on_order(self, order):
        """
        Order event push.
        Order event of a specific vt_orderid is also pushed.
        """
        self.on_event(EVENT_ORDER, order)
        self.on_event(EVENT_ORDER + order.vt_orderid, order)

    def on_position(self, position):
        """
        Position event push.
        Position event of a specific vt_symbol is also pushed.
        """
        self.on_event(EVENT_POSITION, position)
        self.on_event(EVENT_POSITION + position.vt_symbol, position)

    def on_account(self, account):
        """
        Account event push.
        Account event of a specific vt_accountid is also pushed.
        """
        self.on_event(EVENT_ACCOUNT, account)
        self.on_event(EVENT_ACCOUNT + account.vt_accountid, account)

    def on_log(self, log):
        """
        Log event push.
        """
        self.on_event(EVENT_LOG, log)

    def on_contract(self, contract):
        """
        Contract event push.
        """
        self.on_event(EVENT_CONTRACT, contract)

    def write_log(self, msg):
        """
        Write a log event from gateway.
        """
        #log = LogData(msg=msg, gateway_name=self.gateway_name)
        log = LogData()
        log.msg = msg
        log.gateway_name = self.gateway_name
        self.on_log(log)

    def connect(self, setting):
        """
        Start gateway connection.

        to implement this method, you must:
        * connect to server if necessary
        * log connected if all necessary connection is established
        * do the following query and response corresponding on_xxxx and write_log
            * contracts : on_contract
            * account asset : on_account
            * account holding: on_position
            * orders of account: on_order
            * trades of account: on_trade
        * if any of query above is failed,  write log.

        future plan:
        response callback/change status instead of write_log

        """
        pass

    def close(self):
        """
        Close gateway connection.
        """
        pass

    def subscribe(self, req):
        """
        Subscribe tick data update.
        """
        pass


    def send_order(self, req):
        """
        Send a new order to server.

        implementation should finish the tasks blow:
        * create an OrderData from req using OrderRequest.create_order_data
        * assign a unique(gateway instance scope) id to OrderData.orderid
        * send request to server
            * if request is sent, OrderData.status should be set to Status.SUBMITTING
            * if request is failed to sent, OrderData.status should be set to Status.REJECTED
        * response on_order:
        * return OrderData.vt_orderid

        :return str vt_orderid for created OrderData
        """
        pass

    def cancel_order(self, req):
        """
        Cancel an existing order.
        implementation should finish the tasks blow:
        * send request to server
        """
        pass

    def send_orders(self, reqs):
        """
        Send a batch of orders to server.
        Use a for loop of send_order function by default.
        Reimplement this function if batch order supported on server.
        """
        vt_orderids = []

        for req in reqs:
            vt_orderid = self.send_order(req)
            vt_orderids.append(vt_orderid)

        return vt_orderids

    def cancel_orders(self, reqs):
        """
        Cancel a batch of orders to server.
        Use a for loop of cancel_order function by default.
        Reimplement this function if batch cancel supported on server.
        """
        for req in reqs:
            self.cancel_order(req)


    def query_account(self):
        """
        Query account balance.
        """
        pass

    def query_position(self):
        """
        Query holding positions.
        """
        pass

    def query_history(self, req):
        """
        Query bar history data.
        """
        pass

    def get_default_setting(self):
        """
        Return default setting dict.
        """
        return self.default_setting

'''
only to record 
'''
class RedisRabbitmqGateway(BaseGateway):
    def __init__(self, event_engine , gateway_name ):
        super(HuobiGateway,self).__init__(event_engine, gateway_name)


    def on_tick(self, tick):
        print("on_tick")
        print(tick.__dict__)
    
    def on_rest_tick(self, tick):
        print("on_rest_tick")
        print(tick.__dict__)
