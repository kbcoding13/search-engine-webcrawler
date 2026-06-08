import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import base64

load_dotenv()

class GitHubFetcher:
    def __init__(self, owner, repo):
        self.token = os.getenv("GIT_AUTHORIZATION_TOKEN")
        self.endpoint = f"https://api.github.com/repos/{owner}/{repo}"
        self.readme = self.endpoint + "/readme"
        self.keys = ["name", "topics", "stargazers_count", "language", "html_url", "description"]
        self.content = {}
        self.query = []

    def _get(self, url):
        try:
            response = requests.get(url, headers={"Accept": "application/vnd.github+json", "Authorization": f"token {self.token}", "X-GitHub-Api-Version": "2022-11-28"})
            if response.status_code == 200:
                data = response.json()
                return data
        except requests.exceptions.RequestException as e:
            return f"A network error has occured"

    def fetch_readme(self):
        data = self._get(self.readme)
        bytes = base64.b64decode(data['content'])
        text = bytes.decode('utf-8')
        return text

    def fetch_importants(self):
        data = self._get(self.endpoint)
        for i in range(len(self.keys)):
            self.content[self.keys[i]] = data[self.keys[i]]
        return self.content
    
    def search_repos(self, query):
        search_endpoint = f"https://api.github.com/search/repositories?q={query}"
        data = self._get(search_endpoint)
        for item in data['items']:
            cont = {}
            for i in range(len(self.keys)):
                cont[self.keys[i]] = item[self.keys[i]]
            self.query.append(cont)
        return self.query

git_fetch = GitHubFetcher("chrislgarry", "Apollo-11")
print(git_fetch.search_repos("machine_learning"))