import json
import os

class BookManager:
    def __init__(self, filename='storage.json'):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return []

    def save_books(self):
        with open(self.filename, 'w') as f:
            json.dump(self.books, f, indent=2)

    def add_book(self, title, total_pages):
        for book in self.books:
            if book['title'] == title:
                return  # Avoid duplicates
        self.books.append({
            'title': title,
            'total_pages': total_pages,
            'last_page': 0
        })
        self.save_books()

    def update_page(self, title, page):
        for book in self.books:
            if book['title'] == title:
                book['last_page'] = page
                break
        self.save_books()
