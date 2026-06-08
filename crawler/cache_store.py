import redis
from cassandra.cluster import Cluster
import datetime as dt
import uuid

class ContentCache:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)

    def set_cache(self, host, parse):
        self.r.set(host, parse, ex=43200)

    def get_cache(self, host):
        return self.r.get(host)
    
class ContentStorage:
    def __init__(self):
        self.perma_storage = {}
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
            self.session.execute("CREATE TABLE IF NOT EXISTS cache.names ( cache_id uuid, url text, content text, crawled_at timestamp, PRIMARY KEY (cache_id))")

    def store(self, url, parse):
        self.row = self.session.execute(f"""INSERT INTO cache.names (cache_id, url, content, crawled_at)
                                        VALUES (%s, %s, %s, %s)""", (uuid.uuid4() ,url, parse, dt.datetime.now()))

    def release(self, url):
        cache = self.session.execute(f"SELECT * FROM cache.names WHERE url = '{url}' ")
        return cache
    

