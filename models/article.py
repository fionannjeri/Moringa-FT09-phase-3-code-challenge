from database.connection import CONN, CURSOR
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, author, magazine, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string")
        if not 5 <= len(title) <= 50:
            raise ValueError("Title must be between 5 and 50 characters")
            
        self._id = None
        self._title = title
        self._author_id = author.id
        self._magazine_id = magazine.id
        
        # Create entry in database
        CURSOR.execute(
            "INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
            (title, self._author_id, self._magazine_id)
        )
        CONN.commit()
        self._id = CURSOR.lastrowid

    @property
    def title(self):
        if not hasattr(self, '_title'):
            CURSOR.execute(
                "SELECT title FROM articles WHERE id = ?",
                (self.id,)
            )
            self._title = CURSOR.fetchone()[0]
        return self._title

    @property
    def author(self):
        CURSOR.execute("""
            SELECT authors.* FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.id = ?
        """, (self.id,))
        return Author.from_db(CURSOR.fetchone())

    @property
    def magazine(self):
        CURSOR.execute("""
            SELECT magazines.* FROM magazines
            JOIN articles ON articles.magazine_id = magazines.id
            WHERE articles.id = ?
        """, (self.id,))
        return Magazine.from_db(CURSOR.fetchone())

    @classmethod
    def from_db(cls, row):
        # Helper method to create instance from database row
        article = cls.__new__(cls)
        article._id = row[0]
        article._title = row[1]
        article._author_id = row[2]
        article._magazine_id = row[3]
        return article