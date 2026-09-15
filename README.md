# Search Engine

A small web search engine in Python. It crawls news pages, stores and caches what it finds, ranks pages for a query with BM25, and suggests search terms as you type.

The crawler starts from the BBC News sitemap. `app.py` runs the whole pipeline once, with the query `"Liverpool"` and the autocomplete prefix `"Liv"` hard-coded.

## How it works

```
sitemap ─► FrontQueue ─► BackQueue ─► HTML_Fetcher ─► HTML_Parser
                                                          │
          ┌───────────────┬───────────────┬───────────────┼───────────────┐
          ▼               ▼               ▼               ▼               ▼
  DuplicateDetection  Redis cache    Cassandra     Kafka producer    URLFilter /
  (MD5 + MinHash)    (ContentCache) (ContentStorage)      │            URLSeen
                                                          ▼
                                            Kafka consumer ─► ImageDownloader
                                                          └─► BackgroundIndexer ─► Trie
```

1. **URL frontier**: `FrontQueue` reads the sitemap and puts the newest articles first. `BackQueue` groups URLs by host and waits at least 10 seconds between requests to the same host.
2. **Fetch and parse**: `HTML_Fetcher` downloads each page (3-second timeout). `HTML_Parser` pulls out the text, links and image URLs.
3. **Duplicate check**: `DuplicateDetection` catches exact copies with an MD5 fingerprint, and near-copies with MinHash (Jaccard similarity of 0.95 or more).
4. **Storage**:
   - Redis caches page text and query results for 12 hours.
   - Cassandra stores pages permanently, spread across 4 shards by an MD5 hash of the URL (`crawler/shard.py`).
5. **Streaming**: each crawled page is sent to the Kafka topic `crawled_pages`. A consumer reads it back to download images into `images/`. `BackgroundIndexer` runs in a background thread and adds new words to the autocomplete trie.
6. **Ranking**: `Rank` scores the stored pages against the query with BM25 (`rank_bm25`). Results are cached in Redis and can be paginated with `QueryOutput`.
7. **Autocomplete**: `Populate` splits text into words with NLTK and drops stopwords. The words go into a `Trie`, which is searched by prefix.

## Project layout

| Path | Contents |
| --- | --- |
| `app.py` | Entry point that runs the whole pipeline |
| `crawler/url_frontier.py` | `FrontQueue` (orders URLs by priority) and `BackQueue` (limits requests per host) |
| `crawler/html_fetchrend.py` | `HTML_Fetcher`: downloads pages over HTTP |
| `crawler/html_parser.py` | `HTML_Parser`: extracts text, links and images with BeautifulSoup |
| `crawler/dup_det.py` | `DuplicateDetection`: finds exact and near-duplicate pages |
| `crawler/cache_store.py` | `ContentCache` (Redis) and `ContentStorage` (Cassandra) |
| `crawler/shard.py` | `Shard`: picks a shard from a hash of the URL |
| `crawler/kafka_store.py` | Kafka producer and consumer, plus `BackgroundIndexer` |
| `crawler/modular.py` | `ImageDownloader` and `AnaylticsService` (counts links and words, reads page metadata) |
| `crawler/url_filter.py` | `URLFilter`: rejects non-HTTPS URLs, file downloads, fragments and query strings |
| `crawler/url_seendetector.py` | `URLSeen`: remembers which URLs were already visited |
| `text_transformation/rank.py` | `Rank`: BM25 ranking |
| `text_transformation/query.py` | `QueryOutput`: builds and paginates results, limits requests to one per 10 seconds |
| `autocomplete/populate.py` | `Populate`: NLTK word splitting with stopwords removed |
| `autocomplete/trie.py` | `Trie`: prefix search |
| `api/` | Standalone fetchers for GitHub, Medium, Reddit and Wikipedia |

## Requirements

- Python 3.10
- Redis on `localhost:6379`
- Apache Cassandra on `127.0.0.1:9042`
- Apache Kafka on `localhost:9092`

On Windows, the services can run inside WSL. `localhost` in WSL is reachable from Windows.

## Setup

### 1. Create a virtual environment and install packages

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Download the NLTK data

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt'); nltk.download('punkt_tab')"
```

### 3. Start the services

```bash
# Redis
sudo service redis-server start

# Cassandra
sudo service cassandra start

# Kafka (KRaft mode). Format the storage once, then start the server.
KAFKA_CLUSTER_ID=$(bin/kafka-storage.sh random-uuid)
bin/kafka-storage.sh format -t $KAFKA_CLUSTER_ID -c config/server.properties
bin/kafka-server-start.sh config/server.properties
```

`ContentStorage` creates the Cassandra keyspace `cache` and the table `cache.names` the first time it runs.

### 4. Configure API keys (only needed for `api/`)

Create `api/.env`:

```env
GIT_AUTHORIZATION_TOKEN=your_github_token
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

This file is gitignored. Never commit it.

## Running

```bash
python app.py
```

This reads the BBC News sitemap, takes the 8 newest articles, and then for each one:

- fetches the page and stores it
- sends it to Kafka and downloads its images
- ranks the stored pages for `"Liverpool"`
- prints the first 5 autocomplete suggestions for `"Liv"`

To try a different query or seed URL, edit `endpoint` and the hard-coded strings in `app.py`.

Each file in `api/` runs a sample request when you run it directly, for example `python api/wiki_fetcher.py`.

## Notes

- Downloaded images go to `images/`, which is gitignored.
- `autocomplete/populate.py` and the `api/` modules run sample code when they are imported. `app.py` imports `populate.py`, so its sample output prints at startup.
