class URLSeen:
    def __init__(self):
        self.visited_urls = set()

    def check_seen(self, url):
        if url in self.visited_urls:
            return True
        else:
            self.visited_urls.add(url)
            return False