from database.connection import CONN, CURSOR
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id, name):
        # Validate name
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")
            
        self._id = None
        self._name = name
        
        # Create entry in database
        CURSOR.execute(
            "INSERT INTO authors (name) VALUES (?)",
            (name,)
        )
        CONN.commit()
        self._id = CURSOR.lastrowid

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        if not hasattr(self, '_name'):
            # Fetch from database
            CURSOR.execute(
                "SELECT name FROM authors WHERE id = ?",
                (self.id,)
            )
            self._name = CURSOR.fetchone()[0]
        return self._name

    def articles(self):
        CURSOR.execute("""
            SELECT articles.* FROM articles
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        """, (self.id,))
        return [Article.from_db(row) for row in CURSOR.fetchall()]

    def magazines(self):
        CURSOR.execute("""
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            JOIN authors ON articles.author_id = authors.id
            WHERE authors.id = ?
        """, (self.id,))
        return [Magazine.from_db(row) for row in CURSOR.fetchall()]

    @classmethod
    def from_db(cls, row):
        # Helper method to create instance from database row
        author = cls.__new__(cls)
        author._id = row[0]
        author._name = row[1]
        return author