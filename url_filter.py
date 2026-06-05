from pathlib import Path

class URLFilter:
    def __init__(self):
        pass

    def is_valid(self, url):
        if self.check_start(url):
            if self.check_filetype(url):
                if self.check_fragments(url):
                    if self.check_query(url):
                        return True
        return False


    def check_start(self, url):
        if url.startswith('https'):
            return True
        return False
    
    def check_filetype(self, url):
        if url.endswith(('.pdf', '.zip', '.exe', '.jpg')):
            return False
        return True

    def check_fragments(self, url):
        if '#' in url:
            return False
        return True
    
    def check_query(self, url):
        if '?' in url:
            return False
        return True