import json
import re

import bs4
import requests
from sqlalchemy.orm import Session

from models import setup_db, Post, engine


class Scraper(object):

    def __init__(self):
        self.author_cache = {}

    def save_to_db(self, article_titles, article_contents, article_hrefs, article_authors):
        for title, content, url, author in zip(article_titles, article_contents, article_hrefs, article_authors):
            with Session(engine) as session:
                query = session.query(Post).filter_by(author=author, title=title)
                res = query.all()
                if len(res) == 0:
                    post = Post(
                        title=title, content=content, url=url, author=author
                    )
                    session.add(post)
                    session.commit()

    def scrape_data(self):
        url = "https://techcrunch.com/"
        response = requests.get(url)
        soup = bs4.BeautifulSoup(response.text, "html.parser")
        article_titles, article_contents, article_hrefs, article_authors = [], [], [], []

        for tag in soup.findAll("div", {"class": "post-block post-block--image post-block--unread"}):
            tag_header = tag.find("a", {"class": "post-block__title__link"})
            tag_content = tag.find("div", {"class": "post-block__content"})
            article_title = tag_header.get_text().strip()
            article_href = tag_header["href"]
            article_content = tag_content.get_text().strip()
            article_author = tag.find("span", {"class": "river-byline__authors"}).get_text().strip()
            article_author = re.sub("\t\n", " ", article_author)
            article_titles.append(article_title)
            article_contents.append(article_content)
            article_hrefs.append(article_href)
            article_authors.append(article_author)

        return article_titles, article_contents, article_hrefs, article_authors

    def scrape(self):
        article_titles, article_contents, article_hrefs, article_authors = self.scrape_data()
        self.save_to_db(article_titles, article_contents, article_hrefs, article_authors)
        return str(article_titles)

    def scrape_api(self):
        url = "https://techcrunch.com/wp-json/tc/v1/magazine?page="
        pagecount = 10
        res = 0
        for i in range(1, pagecount):
            main_url = url + str(i)
            response = requests.get(main_url)
            data = response.json()
            res += (self.parse_page(data))
            if res >= 100:
                break
        return str(res)

    def parse_page(self, data):
        article_ids, article_titles, article_contents, article_hrefs, article_authors = [], [], [], [], []
        res = []
        for item in data:
            article_ids.append(item['id'])
            article_titles.append(item['title']['rendered'])
            article_contents.append(item['content']['rendered'])
            article_hrefs.append(item['link'])
            article_authors.append(self.get_author(item['author']))
        self.save_to_db(article_titles, article_contents, article_hrefs, article_authors)
        return len(article_ids)

    def get_author(self, author_id):
        if author_id in self.author_cache.keys():
            return self.author_cache.get(author_id)
        else:
            try:
                url = "https://techcrunch.com/wp-json/tc/v1/users/" + str(author_id)
                response = requests.get(url)
                data = response.json()
                author_name = data['name']
                self.author_cache[author_id] = author_name
                return author_name
            except Exception as e:
                print(e)
                return author_id
