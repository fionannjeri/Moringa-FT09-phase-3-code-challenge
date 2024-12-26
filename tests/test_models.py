import unittest
from models.author import Author
from models.magazine import Magazine
from models.article import Article
from database.connection import CONN, CURSOR

class TestModels(unittest.TestCase):
    def setUp(self):
        # Clear all tables before each test
        CURSOR.execute("DELETE FROM articles")
        CURSOR.execute("DELETE FROM authors")
        CURSOR.execute("DELETE FROM magazines")
        CONN.commit()

    def test_author_creation(self):
        author = Author(None, "John Doe")
        self.assertIsInstance(author.id, int)
        self.assertEqual(author.name, "John Doe")

    def test_magazine_creation(self):
        magazine = Magazine(None, "Tech Weekly", "Technology")
        self.assertIsInstance(magazine.id, int)
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_article_creation(self):
        author = Author(None, "John Doe")
        magazine = Magazine(None, "Tech Weekly", "Technology")
        article = Article(author, magazine, "Python Tips")
        
        self.assertIsInstance(article.id, int)
        self.assertEqual(article.title, "Python Tips")
        self.assertEqual(article.author.name, "John Doe")
        self.assertEqual(article.magazine.name, "Tech Weekly")

    def test_relationships(self):
        author = Author(None, "John Doe")
        magazine = Magazine(None, "Tech Weekly", "Technology")
        
        Article(author, magazine, "Python Tips")
        Article(author, magazine, "JavaScript Basics")
        
        self.assertEqual(len(author.articles()), 2)
        self.assertEqual(len(magazine.articles()), 2)
        self.assertEqual(len(author.magazines()), 1)
        self.assertEqual(len(magazine.contributors()), 1)

if __name__ == '__main__':
    unittest.main()