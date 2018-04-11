import os
import hashlib
from flask import request
from werkzeug.contrib.cache import NullCache, RedisCache
from redis.connection import ResponseError


def make_cache_key_request_args():
    """Create consistent keys for query string arguments.
    Produces the same cache key regardless of argument order, e.g.,
    both `?limit=10&offset=20` and `?offset=20&limit=10` will
    always produce the same exact cache key.
    """

    # Create a tuple of (key, value) pairs, where the key is the
    # argument name and the value is its respective value. Order
    # this tuple by key. Doing this ensures the cache key created
    # is always the same for query string args whose keys/values
    # are the same, regardless of the order in which they are
    # provided.
    args_as_sorted_tuple = tuple(
        sorted(
            (pair for pair in request.args.items(multi=True))
        )
    )
    # ... now hash the sorted (key, value) tuple so it can be
    # used as a key for cache. Turn them into bytes so that md5
    # will accept them
    args_as_bytes = str(args_as_sorted_tuple).encode()
    hashed_args = str(hashlib.md5(args_as_bytes).hexdigest())
    return hashed_args


class fastNullCache(NullCache):
    def delete(self, key, wildcard=False):
        return True


class fastRedisCache(RedisCache):

    def delete(self, key, wildcard=False):
        if not wildcard:
            return self._client.delete(self.key_prefix + key)
        else:
            try:
                self._client.eval(
                    '''return redis.call('del', unpack(redis.call('keys', ARGV[1])))''', 0, '{}:*'.format(key))
            except ResponseError:
                pass


class FastCache(object):
    def setup():
        cache_type = os.environ.get('CACHE_TYPE', 'null')
        if cache_type == 'redis':
            cache_host = os.environ.get('CACHE_REDIS_HOST', 'localhost')
            cache_port = os.environ.get('CACHE_REDIS_PORT', 6379)
            return fastRedisCache(host=cache_host, port=cache_port)
        else:
            return fastNullCache()
