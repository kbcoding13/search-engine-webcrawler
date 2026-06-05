import hashlib
from datasketch import MinHash

class DuplicateDetection():
    def __init__(self):
        self.fingerprints = set()
        self.minhash_signatures = list()

    def get_fingerprint(self, text):
        byte_string = text.encode('utf-8')
        return hashlib.md5(byte_string).hexdigest()
    
    def check_exact(self, page):
        self.fingerprint = self.get_fingerprint(page)
        if self.fingerprint in self.fingerprints:
            return True
        else:
            self.fingerprints.add(self.fingerprint)
            self.check_near(page)

    def check_near(self, p1):
        new_hash = MinHash()
        for h in p1.split():
            new_hash.update(h.encode('utf-8'))
        for item in self.minhash_signatures:
            similarity = new_hash.jaccard(item)
            if similarity >= 0.95:
                return True
        self.minhash_signatures.append(new_hash)
        return False
    