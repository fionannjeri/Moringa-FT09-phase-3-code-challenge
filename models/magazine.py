from database.connection import CONN, CURSOR
from models.article import Article
from models.author import Author

class Magazine:
    def __init__(self, id, name, category):
        # Validate name
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not 2 <= len(name) <= 16:
            raise ValueError("Name must be between 2 and 16 characters")
            
        # Validate category
        if not isinstance(category, str):
            raise TypeError("Category must be a string")
        if len(category) == 0:
            raise ValueError("Category must be longer than 0 characters")
            
        self._id = None
        self._name = name
        self._category = category
        
        # Create entry in database
        CURSOR.execute(
            "INSERT INTO magazines (name, category) VALUES (?, ?)",
            (name, category)
        )
        CONN.commit()
        self._id = CURSOR.lastrowid

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not 2 <= len(value) <= 16:
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value
        CURSOR.execute(
            "UPDATE magazines SET name = ? WHERE id = ?",
            (value, self.id)
        )
        CONN.commit()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0 characters")
        self._category = value
        CURSOR.execute(
            "UPDATE magazines SET category = ? WHERE id = ?",
            (value, self.id)
        )
        CONN.commit()

    def articles(self):
        CURSOR.execute("""
            SELECT articles.* FROM articles
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """, (self.id,))
        return [Article.from_db(row) for row in CURSOR.fetchall()]

    def contributors(self):
        CURSOR.execute("""
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON articles.author_id = authors.id
            JOIN magazines ON articles.magazine_id = magazines.id
            WHERE magazines.id = ?
        """, (self.id,))
        return [Author.from_db(row) for row in CURSOR.fetchall()]

    def article_titles(self):
        articles = self.articles()
        if not articles:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        CURSOR.execute("""
            SELECT authors.*, COUNT(articles.id) as article_count 
            FROM authors
            JOIN articles ON articles.author_id = authors.id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        """, (self.id,))
        results = CURSOR.fetchall()
        if not results:
            return None
        return [Author.from_db(row) for row in results]

    @classmethod
    def from_db(cls, row):
        # Helper method to create instance from database row
        magazine = cls.__new__(cls)
        magazine._id = row[0]
        magazine._name = row[1]
        magazine._category = row[2]
        return magazine