import requests
import base64

class RedditFetcher():
    def __init__(self):
        self.endpoint = "https://www.reddit.com/r/"

    def _get(self, url):
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 search-engine-crawler by /u/UnintelligentSheep"})
            if response.status_code == 200:
                data = response.json()
                return data
            return response.status_code
        except requests.exceptions.RequestException as e:
            return f"This subreddit doesn't exist. Try again"

    def search_sub(self, query:str):
        url = self.endpoint + query + ".json"
        data = self._get(url)  
        return data
    
red_fetch = RedditFetcher()
print(red_fetch.search_sub("PewdiepieSubmissions"))

