import redis
from random import choice
# from setting import MAX_SCORE,MIN_SCORE,INITAL_SCORE, REDIS_HOST, REDIS_PORT, REDIS_KEY, PASSWOR

# redis info
from travel_spider.settings import *
MAX_SCORE = 100
MIN_SCORE = 0
INITAL_SCORE = 10
# REDIS_HOST = '192.168.25.65'
# REDIS_PORT = 6379
PASSWOR = None
REDIS_KEY = 'ctrip:cookies'


class PoolEmptyError(Exception):

    def __init__(self):
        Exception.__init__(self)

    def __str__(self):
        return repr('cookie池已经枯竭')


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=None):
        """
        :param host : ip for redis
        :param port : port for redis
        :param password: for redis
        :return:
        """
        self.db = redis.StrictRedis(host=host, port=port, decode_responses=True)

    def add(self, proxy, score=INITAL_SCORE):
        '''
        :param proxy: proxy
        :param score: inital score
        :return zadd result
        '''
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        '''
        random get valid proxy order by score
        '''

        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        '''
        :param proxy:decrease score for the proxy, or delete
        '''
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score - 30 > MIN_SCORE:
            print('proxy ', proxy, ' current score is ', score, ' decrease 1')
            return self.db.zincrby(REDIS_KEY, proxy, -30)
        else:
            print('remove proxy :' + proxy)
            return self.db.zrem(REDIS_KEY, proxy)

    def rem(self, proxy):
        return self.db.zrem(REDIS_KEY, proxy)

    def exists(self, proxy):
        '''
        if exists
        :param proxy:
        :return
        '''

        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        '''
        set the proxy max score
        :param proxy:
        :return
        '''
        print('proxy ', proxy, ' valid, set score ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        '''
        get the count of proxies
        :return
        '''
        return self.db.zcard(REDIS_KEY)

    def all(self):
        '''
        get all proxy
        :return
        '''
        return self.db.zrangebyscore(REDIS_KEY, -20, MAX_SCORE)

    def valid_proxies(self):
        '''
        get all proxy
        :return
        '''
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MIN_SCORE-1)

    def add_hash(self, redis_key, field, value):
        '''
        添加hash表元素
        :param redis_key:
        :param field:
        :param value:
        :return:
        '''
        return self.db.hset(redis_key, field, value)

    def del_hash(self, redis_key, fields):
        '''
        删除hash表中的元素
        :param redis_key:
        :param field:
        :param value:
        :return:
        '''
        return self.db.hdel(redis_key, fields)

    def get_hash(self, redis_key, field):
        '''
        获取hash表中的元素
        :param redis_key:
        :param field:
        :return:
        '''
        return self.db.hget(redis_key, field)

    def count_hash(self, redis_key):

        return self.db.hlen(redis_key)

if __name__ == '__main__':
    rd = RedisClient(REDIS_HOST, REDIS_PORT)
    rd.add_hash('ctrip', 'main2', 'test')
    print(rd.get_hash('ctrip', 'main'))
    print(rd.count_hash('ctrip'))

