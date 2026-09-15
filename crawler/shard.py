import hashlib

class Shard:
    def __init__(self, num_shards=4):
        self.num_shards = num_shards

    def get_shard(self, url):
        hash_val = int(hashlib.md5(url.encode()).hexdigest(), 16)
        return hash_val % self.num_shards
