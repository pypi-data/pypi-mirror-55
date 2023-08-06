
from django.core.cache import cache
from django_redis.client import DefaultClient
from rediscluster import RedisCluster


#测试
def main():
    cache.set('keya', 'value of key a', 1000)
    cache.set('keyb', 'value of key b', 1000)
    # cache.incr_version('keyb', 5)
    # cache.add('keya', 'a')
    # cache.persist('keya')
    # cache.expire('keya', 100)
    # cache.lock('keya')
    # cache.delete('keya')
    # cache.delete_pattern('*')
    # cache.delete_many(['keya', 'keyb'])
    # cache.clear()
    # result = cache.get_many(['keya', 'keyb'])
    # cache.set_many({"keyc": 'value of key c', "keyd": "value of key d"})
    # cache.incr("keya", 'aaa')
    # result = cache.has_key("keya")
    # result = cache.iter_keys("*")
    # result = cache.keys("*")
    result = cache.close()
    from ipdb import set_trace;set_trace(context=20)


if __name__ == "__main__":
    main()
