import json

from flask import Flask, jsonify
from sqlalchemy.orm import Session

from models import setup_db, engine, Post
from scraper import Scraper

server = Flask(__name__)
scraper = Scraper()


@server.get("/")
def hello():
    return jsonify({
        'get_articles_by_author_name': 'http://localhost:8000/get_articles_by_author_name/Manish%20Singh',
        'toscrape': 'http://localhost:8000/scrape'})


@server.get("/scrape")
def scrape():
    return scraper.scrape_api()


@server.get("/get_articles_by_author_name/<author>")
def get_articles_by_author_name(author):
    with Session(engine) as session:
        query = session.query(Post).filter_by(author=author)
        result = query.all()
        result_list = []
        for res in result:
            result_list.append(
                {"id": res.id, "title": res.title, "author": res.author, "content": res.content, "url": res.url})
        return json.dumps(result_list)


@server.get("/get_first_post/")
def get_first_post():
    with Session(engine) as session:
        res = session.query(Post).first()
        return json.dumps(
            {"id": res.id, "title": res.title, "author": res.author, "content": res.content, "url": res.url})


if __name__ == "__main__":
    setup_db()
    server.run(host="localhost", port=8000, debug=True, threaded=True)
