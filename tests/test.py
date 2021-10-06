import json

from models import setup_db
from sqlalchemy.orm import Session

from models import setup_db, Post, engine


def test_index(app, client):
    res = client.get('/')
    assert res.status_code == 200
    expected = {'get_articles_by_author_name': 'http://localhost:8000/get_articles_by_author_name/Manish%20Singh',
                'toscrape': 'http://localhost:8000/scrape'}
    assert expected == json.loads(res.get_data(as_text=True))


def setup():
    setup_db()
    with Session(engine) as session:
        author = 'abc'
        title = 'demo'
        content = 'demo content'
        url = 'demourl'
        query = session.query(Post).filter_by(author=author, title=title)
        res = query.all()
        if len(res) == 0:
            post = Post(
                title=title, content=content, url=url, author=author
            )
            session.add(post)
            session.commit()


def test_get_articles_by_author_name(app, client):
    res = client.get('/get_articles_by_author_name/abc')
    assert res.status_code == 200
    expected = 'demo'
    result = json.loads(res.get_data(as_text=True))[0]['title']
    assert result == expected


def test_scrape(app, client):
    res = client.get('/scrape')
    expected = 100
    assert int(res.get_data()) > expected
