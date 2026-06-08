import requests
from wikipediaapi import Wikipedia, SearchProp, SearchInfo, SearchWhat, SearchQiProfile, SearchSort, ExtractFormat

class WikipediaFetcher:
    def __init__(self):
        self.wiki = Wikipedia(user_agent='Search-Engine-Crawler (merlin@example.com)', language='en', extract_format=ExtractFormat.WIKI)

    def _get(self, page):
        try:
            page_py = self.wiki.page(page)
            return page_py.text
        except requests.exceptions.RequestException as e:
            return f"A network error has occured"
        
    def search(self, query:str):
        try:
            results = self.wiki.search(query, 
                                       prop=[SearchProp.SIZE, SearchProp.WORDCOUNT, SearchProp.TIMESTAMP],
                                       info=[SearchInfo.TOTAL_HITS, SearchInfo.SUGGESTION],
                                       what=SearchWhat.TEXT,
                                       qi_profile=SearchQiProfile.ENGINE_AUTO_SELECT,
                                       sort=SearchSort.RELEVANCE,
                                       limit=5)
            return results
        except requests.exceptions.RequestException as e:
            return f"A network error has occured"
    
wiki_fetch = WikipediaFetcher()
print(wiki_fetch.search("Raphinha"))

