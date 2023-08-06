#!/usr/bin/python

# -*- coding:utf-8 -*-

# __author__ = 'Jack'

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)

r = redis.Redis(connection_pool=pool, max_connections=10)

r.flushall()  # 清空Redis

r.setex('name', value='liaogx', time=2)  # 设置新值，过期时间为3s
r.mset(k1 = 'v1', k2 = 'v2', k3 = 'v3')  # 批量设置新值
print(r.mget('k1', 'k2', 'k3', 'k4'))  # 批量获取新值
print(r.getset('name', 'liaogaoxiang'))  # 设置新值并获取原来的值
print(r.getrange('name', 0, 1))  # 获取子序列 0 <= x <= 1

r.setrange('name', 0, 'LIAO')  # 修改字符串内容，从指定字符串索引开始向后替换（新值太长时，则向后添加），返回值的长度

i = 0

while i < 4:
    print(r.get('name'))
    time.sleep(1)
    i += 1

source = 'foo'
r.set('n1', source)
r.setbit('n1', 7, 1)
'''

注：如果在Redis中有一个对应： n1 = "foo"，

    那么字符串foo的二进制表示为：01100110 01101111 01101111

    所以，如果执行 setbit('n1', 7, 1)，则就会将第7位设置为1，

    那么最终二进制则变成 01100111 01101111 01101111，即："goo"

'''
print(r.get('n1'))
print(r.getbit('n1', 7))  # 获取n1对应的值的二进制表示中的某位的值 （0或1）
r.set('n2', '廖高祥')
print(r.strlen('n2'))  # 返回对应的字节长度（一个汉字3个字节）
r.set('num', 1)
r.incr('num', amount=10)
r.decr('num', amount=1)
print(r.get('num'))  # 自增num对应的值，当name不存在时，则创建name＝amount，否则，则自增。
r.append('num', 111)
print(r.get('num'))  # 在redis num对应的值后面追加内容