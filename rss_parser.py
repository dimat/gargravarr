import logging
from bs4 import BeautifulSoup
import requests
import feedparser


class RSSParser:
    """
    Parse an RSS feed and call the handler for each entry.
    """

    def __init__(self, link, name, registry, selector="article"):
        self.link = link
        self.name = name
        self.registry = registry
        self.selector = selector

    def parse(self, handler):
        logging.debug(f"parsing {self.name}")

        feed = feedparser.parse(self.link)
        for entry in feed.entries:
            if self.registry.check_entry_exists(entry.id, self.name):
                continue

            try:
                r = requests.get(entry.link)
                soup = BeautifulSoup(r.text, 'html.parser')
                body = soup.select_one(self.selector)
                if body:
                    entry["downloaded_body"] = body.text
            except Exception as e:
                logging.error(f"Error downloading body for {entry.link}: {e}")

            handler(entry)
            self.registry.store_entry(entry.id, self.name)
