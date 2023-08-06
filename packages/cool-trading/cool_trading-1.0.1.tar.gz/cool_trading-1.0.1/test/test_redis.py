# coding=utf-8

import redis

def test1():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set("a","b")
    r.get("a")

    r.hset("h1","r","s")
    r.hget("h2","r","s")

    r.hincrby("hash1", "k3", amount=-1)
    print(r.hgetall("hash1"))

    r.hset("hash1", "k5", "1.0")

    r.lpush("list1", 11, 22, 33)

    r.rpush("list2", 44, 55, 66)    # 在列表的右边，依次添加44,55,66

    print(r.llen("list2"))  # 列表长度
    
    print(r.lrange("list2", 0, -1)) # 切片取出值，范围是索引号0到-1(最后一个元素)



if __name__ == "__main__":
    test1()