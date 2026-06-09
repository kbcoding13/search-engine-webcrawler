import advertools as adv
import pandas as pd
import datetime as dt
from urllib.parse import urlsplit

class BackQueue:
    def __init__(self):
        self.url_groups = {}
        self.last_fetched = {}
    
    def host(self, url):
        return urlsplit(url).hostname

    #Function for grouping url by host
    def group_url(self, url):
        if self.host(url) in self.url_groups:
            self.url_groups[self.host(url)].append(url)
        else:
            self.url_groups[self.host(url)] = [url]

    #Function for storing the last fetch time per host
    def get_datetime(self, url):
        self.last_fetched[self.host(url)] = dt.datetime.now()

    def check_time(self, url):
        if self.host(url) in self.last_fetched:
            past_time = self.last_fetched[self.host(url)]
            current_time = dt.datetime.now()
            time_difference = current_time - past_time
            if int(time_difference.total_seconds()) >= 10:
                return True
            return False
        else:
            return True
    
    def next_url(self, url):
        return self.url_groups[self.host(url)].pop()

class FrontQueue:
    def __init__(self):
       self.queue = []

    def priority_list(self, url, num: int):
        sitemap_df = adv.sitemap_to_df(url)

        sitemap_df['pub_date'] = pd.to_datetime(sitemap_df['news_publication_date'], errors='coerce', utc=True)
        sitemap_df['hours_since_publish'] = (pd.Timestamp.now(tz='UTC') - sitemap_df['pub_date']).dt.total_seconds() / 3600

        sitemap_df['importance_score'] = 1 / (sitemap_df['hours_since_publish'] + 1)

        url_list = sitemap_df[['loc', 'news_title', 'hours_since_publish', 'importance_score']].sort_values('importance_score', ascending=False).head(num)
        for u in url_list['loc']:
            self.queue.append(u)
        
