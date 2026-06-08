import requests
import os
import datetime as dt
import advertools as adv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class ImageDownloader:
    def __init__(self):
        # self.url = "https://example.com"
        # self.output_path = "downloaded_image.jpg"
        pass
    def download(self, url, output):
        os.makedirs('images', exist_ok=True)
        path = os.path.join('images', output)
        self.response = requests.get(url, stream=True)
        if self.response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in self.response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print("Image downloaded successfully")
    
        else:
            print(f"Failed to download image. Status code: {self.response.status_code}")

class AnaylticsService:
    def __init__(self, fetch, page, sitemap):
        self.analysis = {}
        self.get_count_backlinks(fetch)
        self.get_last_updated(sitemap)
        self.get_word_count(page)
        self.get_metadata(fetch)

    def get_count_backlinks(self, fetch):
        soup = BeautifulSoup(fetch, 'html.parser')

        anchor_tags = soup.find_all('a')

        list_result = []
        for tag in anchor_tags:
            href = tag.get('href')
            if href and href.startswith("http"):
                list_result.append(href)

        total_backlink = len(list_result)
        self.analysis['backlink_count'] = total_backlink

    def get_last_updated(self, sitemap):
        sitemap_df = adv.sitemap_to_df(sitemap)
        sitemap_df['pub_date'] = pd.to_datetime(sitemap_df['news_publication_date'], errors='coerce', utc=True)
        sitemap_df['hours_since_publish'] =  (pd.Timestamp.now(tz='UTC') - sitemap_df['pub_date']).dt.total_seconds() / 3600

        self.analysis['last_updated'] = sitemap_df['hours_since_publish']
    
    def get_word_count(self, page: str):
        word_count = len(page.split())
        self.analysis['word_count'] = word_count
    
    def get_metadata(self, fetch):
        soup = BeautifulSoup(fetch, 'html.parser')
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        key_tag = soup.find('meta', attrs={'name': 'keywords'})

        desc_value = desc_tag['content'] if desc_tag else None
        key_value = key_tag['content'] if key_tag else None

        self.analysis['metadata'] = [key_value, desc_value]
