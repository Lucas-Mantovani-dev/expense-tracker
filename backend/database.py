import sqlite3

def db_init_tables():
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE)"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY,
        amount REAL NOT NULL,
        category_id INTEGER NOT NULL,
        description TEXT,
        date_time DATETIME NOT NULL,
        CONSTRAINT fk_expenses_categories
        FOREIGN KEY (category_id)
        REFERENCES categories(category_id))"""
    )

    conn.commit()
