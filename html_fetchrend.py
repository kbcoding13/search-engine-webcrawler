import requests

class HTML_Fetcher():
    def __init__(self):
        pass
    
    def fetch(self, url):
        try:
            fetched = requests.get(url, timeout=3)
        except requests.exceptions.ConnectionError:
            return None
        except requests.exceptions.Timeout:
            return None
        else:
            if fetched.status_code == 200:
                return fetched.text
            return None