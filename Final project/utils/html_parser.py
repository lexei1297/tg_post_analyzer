import os
from bs4 import BeautifulSoup


class TelegramHTMLParser:
    def __init__(self):
        pass

    def parse_html_files(self, path):
        """
        Parse Telegram HTML files and extract post data.
        """
        posts = []
        if os.path.isfile(path):
            posts.extend(self._parse_single_file(path))
        elif os.path.isdir(path):
            for filename in os.listdir(path):
                if filename.endswith(".html"):
                    file_path = os.path.join(path, filename)
                    posts.extend(self._parse_single_file(file_path))
        else:
            raise ValueError(f"Invalid path: {path}")
        return posts

    def _parse_single_file(self, file_path):
        """
        Parse a single HTML file and extract posts.
        """
        with open(file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")
            posts = []
            for post in soup.find_all("div", class_="tgme_widget_message"):
                date = post.find("time")["datetime"].split("T")[0]
                content = post.find("div", class_="tgme_widget_message_text").text.strip()
                posts.append({"date": date, "content": content})
            return posts
