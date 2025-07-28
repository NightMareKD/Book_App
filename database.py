import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            current_page INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS updates (
            id INTEGER PRIMARY KEY,
            book_id INTEGER,
            page INTEGER,
            timestamp TEXT,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )
    ''')
    conn.commit()
    conn.close()

def add_book(title, total_pages):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("INSERT INTO books (title, total_pages) VALUES (?, ?)", (title, total_pages))
    conn.commit()
    conn.close()

def get_books():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = c.fetchall()
    conn.close()
    return books

def update_page(book_id, page):
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("UPDATE books SET current_page=? WHERE id=?", (page, book_id))
    c.execute("INSERT INTO updates (book_id, page, timestamp) VALUES (?, ?, ?)",
              (book_id, page, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_weekly_stats():
    conn = sqlite3.connect("books.db")
    c = conn.cursor()
    c.execute("""
        SELECT book_id, page, timestamp FROM updates
        WHERE date(timestamp) >= date('now', '-7 day')
    """)
    results = c.fetchall()
    conn.close()
    return results
