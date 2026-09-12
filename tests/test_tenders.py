import tempfile
import unittest
from pathlib import Path

from models.book import Book, BookCollection


class BookTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.books_file = Path(self.temp_dir.name) / "books.json"
        self.collection = BookCollection(self.books_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_book_saves_book(self):
        book = Book("Things Fall Apart", "Chinua Achebe", "Fiction", "Available", "jane@example.com")
        self.collection.add_book(book)
        books = self.collection.view_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Things Fall Apart")

    def test_search_books_by_title(self):
        self.collection.add_book(Book("1984", "George Orwell", "Fiction", "Available", "jane@example.com"))
        self.collection.add_book(Book("Clean Code", "Robert Martin", "Technology", "Available", "jane@example.com"))
        results = self.collection.search_books("clean")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Clean Code")

    def test_update_status(self):
        self.collection.add_book(Book("1984", "George Orwell", "Fiction", "Available", "jane@example.com"))
        updated = self.collection.update_status("1984", "Read")
        self.assertTrue(updated)
        self.assertEqual(self.collection.view_books()[0].status, "Read")

    def test_delete_book(self):
        self.collection.add_book(Book("1984", "George Orwell", "Fiction", "Available", "admin@example.com"))
        deleted = self.collection.delete_book("1984")
        self.assertTrue(deleted)
        self.assertEqual(self.collection.view_books(), [])

    def test_delete_missing_book_returns_false(self):
        self.assertFalse(self.collection.delete_book("Missing"))


if __name__ == "__main__":
    unittest.main()
