from django_redis.client import DefaultClient
from rediscluster import RedisCluster


class RedisClusterClient(DefaultClient):
    def get_client(self, write=True, tried=(), show_index=False):
        client = RedisCluster(startup_nodes=self._server, decode_responses=False)
        if show_index:
            return client, 0
        else:
            return client
