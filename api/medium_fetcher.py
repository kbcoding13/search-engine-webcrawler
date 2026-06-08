from bs4 import BeautifulSoup
import requests

class MediumFetcher:
    def __init__(self):
        self.file = None
        self.values = ['link', 'category', 'dc:creator', 'pubDate', 'atom:updated', 'content:encoded']
        self.content = {}

    def _get(self, url):
        self.file = url
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.text
                return self.rss_feed(data)
        except requests.exceptions.RequestException as e:
            return f"A network error has occured"

    def rss_feed(self, data):
        soup = BeautifulSoup(data, 'xml')
        items = soup.find_all('item')
        for item in items:
            title = item.find('title').text
            self.content[title] = []
            for v in self.values:
                self.content[title].append(item.find_all(v))
        return self.content
        
med_fetch = MediumFetcher()
po = med_fetch._get('https://medium.com/feed/@medium')
print(po)