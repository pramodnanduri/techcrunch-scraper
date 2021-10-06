from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import registry

DB_FILENAME = "scraper.db"
engine = create_engine(f"sqlite:///{DB_FILENAME}")

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(String)
    url = Column(String)
    author = Column(String)

    def __repr__(self):
        return (
            f"Post(id={self.id}, title={self.title}, content={self.content},"
            f" url = {self.url}, author={self.author})"
        )


def setup_db():
    Base.metadata.create_all(engine)
