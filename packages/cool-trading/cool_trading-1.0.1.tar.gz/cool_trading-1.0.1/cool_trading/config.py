# coding=utf-8


#####################################
PREFIX = "bbt_"		# 巴比特

#####################################
#redis config
REDIS_SERVER = '127.0.0.1'
REDIS_PORT = 6379

#####################################
#rabbitmq config
MQ_SERVER = "127.0.0.1"				# rabbtimq_server
MQ_PORT = 5672						# rabbitmq_port
MQ_USER = "admin"					# rabbitmq_user
MQ_PASSWD = "admin"					# rabbitmq_password

FANOUT = "fanout"

#####################################
#redis_key:

REDIS_ORDER_BOOK = "order_book"
REDIS_TICKER = "ticker"

#key_type:[REDIS_ORDER_BOOK , REDIS_TICKER]
def getRedisKey(key_type , exchange):
	return PREFIX + key_type + "_" + exchange

#####################################
#rabbitmq_exchange
MQ_DEPTH = "depth"
MQ_RESTFUL_DEPTH = "restful_depth"

#key_type:[MQ_DEPTH]
def getRabbitExchangeKey(key_type , exchange):
	return PREFIX + "exchange_" + key_type + "_" + exchange

#rabbitmq_send_queue
#key_type:[MQ_DEPTH]
def getRabbitSendQueueKey(key_type , exchange):
	return PREFIX + "send_queue_" + key_type + "_" + exchange

#rabbitmq_receive_queue
#key_type:[MQ_DEPTH]
def getRabbitReceiveQueueKey(key_type, exchange , unique_str):
	return PREFIX + "receive_queue_" + key_type + "_" + exchange + unique_str



if __name__ == "__main__":
	# test
	a = getRabbitExchangeKey(MQ_DEPTH , EXCHANGE_HUOBI)
	print(a)
	