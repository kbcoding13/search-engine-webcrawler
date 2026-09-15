import redis
from cassandra.cluster import Cluster
import datetime as dt
import uuid
from .shard import Shard

class ContentCache:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def set_cache(self, host, parse):
        self.r.set(host, parse, ex=43200)

    def get_cache(self, host):
        return self.r.get(host)
    
class ContentStorage:
    def __init__(self, num_shards=4):
        self.shard = Shard(num_shards)
        try:
            self.cluster = Cluster(['127.0.0.1'])
            self.session = self.cluster.connect()
        except Exception as e:
            print(f"Connection failed: {e}")
        else:
            self.session.execute("""CREATE KEYSPACE IF NOT EXISTS cache
                                 WITH replication = {
                                 'class': 'SimpleStrategy',
                                 'replication_factor': 1
                                 }""")
            self.session.execute("CREATE TABLE IF NOT EXISTS cache.names ( shard_id int, cache_id uuid, url text, content text, crawled_at timestamp, PRIMARY KEY (shard_id, cache_id))")

    def store(self, url, parse):
        shard_id = self.shard.get_shard(url)
        self.session.execute("""INSERT INTO cache.names (shard_id, cache_id, url, content, crawled_at)
                                VALUES (%s, %s, %s, %s, %s)""", (shard_id, uuid.uuid4(), url, parse, dt.datetime.now()))

    def release(self, url):
        shard_id = self.shard.get_shard(url)
        return self.session.execute("SELECT * FROM cache.names WHERE shard_id = %s", (shard_id,))

    def release_content(self):
        content = {}
        for shard_id in range(self.shard.num_shards):
            rows = self.session.execute("SELECT content, url FROM cache.names WHERE shard_id = %s", (shard_id,))
            for c in rows:
                content[c.content] = c.url
        return content