from bs4 import BeautifulSoup
from urllib.parse import urljoin

class HTML_Parser():
    def __init__(self, html):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.feed = []

    def page(self):
        text = self.soup.get_text()
        return text

    def feedback(self, base):
        links = [a['href'] for a in self.soup.find_all('a', href=True)]
        for link in links:
            new_link = urljoin(base, link)
            self.feed.append(new_link)
        return self.feed
    
    def feedback_img(self, base):
        links = [img['src'] for img in self.soup.find_all('img') if img.has_attr('src')]
        for link in links:
            new_link = urljoin(base, link)
            self.feed.append(new_link)
        return self.feed

#  title, author, URL, date, categories, content.