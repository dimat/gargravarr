from bs4 import BeautifulSoup
import requests
import feedparser


class RSSParser:
    def __init__(self, link, name, registry, selector="article"):
        self.link = link
        self.name = name
        self.registry = registry
        self.selector = selector

    def parse(self, handler):
        print(f"parsing {self.name}")
        print(f"==============================")
        feed = feedparser.parse(self.link)
        for entry in feed.entries:
            if self.registry.check_entry_exists(entry.id, self.name):
                continue

            r = requests.get(entry.link)
            soup = BeautifulSoup(r.text, 'html.parser')
            body = soup.select_one(self.selector)
            if body:
                entry["downloaded_body"] = body.text

            handler(entry)
            self.registry.store_entry(entry.id, self.name)
