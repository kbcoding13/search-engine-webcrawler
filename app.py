from crawler.url_frontier import FrontQueue, BackQueue
from crawler.html_fetchrend import HTML_Fetcher
from crawler.html_parser import HTML_Parser
from crawler.dup_det import DuplicateDetection
from crawler.cache_store import ContentCache, ContentStorage
from crawler.kafka_store import KafkaProd, KafkaCons
from crawler.modular import ImageDownloader, AnaylticsService
from crawler.url_filter import URLFilter
from crawler.url_seendetector import URLSeen
import json

from text_transformation.rank import Rank
from text_transformation.query import QueryOutput

# -- SEED URL --

endpoint = 'https://www.bbc.com/sitemaps/https-index-com-news.xml'

# -- URL FRONTIER --

back_queue = BackQueue()
front_queue = FrontQueue()
fetcher = HTML_Fetcher()
dupe = DuplicateDetection()
cache = ContentCache()
storage = ContentStorage()
producer = KafkaProd()
consumer = KafkaCons('1')
image_download = ImageDownloader()
filter = URLFilter()
urlseen = URLSeen()

ranker = Rank()
query_output = QueryOutput()

front_queue.priority_list(endpoint, 8)

for u in front_queue.queue:
    if back_queue.check_time(u):
        back_queue.group_url(u)
        back_queue.get_datetime(u)

print(back_queue.url_groups)
print(back_queue.last_fetched)

url_groups = back_queue.url_groups

# -- HTML FETCHER + PARSER --

for u in url_groups[back_queue.host(endpoint)]:
    result = fetcher.fetch(u)
    parser = HTML_Parser(result)
    page = parser.page()[:200]
    dupe.check_exact(page)

    cache.set_cache(u, page)
    storage.store(u, page)

    img = parser.feedback_img(u)
    producer.produce(u, page, img)

    messages = consumer.consumer.poll(timeout_ms=10000)
    for tp, records in messages.items():
        for c in records:
            c_json = json.loads(c.value)
            for j in c_json['image_url']:
                if j.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                    image_download.download(j, j.split('/')[-1])
    
    analytics = AnaylticsService(result, page, endpoint)
    print(analytics.analysis)

    for p in parser.feed:
        if filter.is_valid(p):
            print('The returned URL is valid')
            if urlseen.check_seen(p):
                print('This has already been visited')
            else:
                print('A new URL has been added to storage')
        else:
            print('The returned URL is not valid')

    content = storage.release_content()
    corpus = list(content)
    
    rank_dict = ranker.rank(corpus, "Liverpool")
    rank_list = list(rank_dict)
    
    print(query_output.output(rank_list, content))