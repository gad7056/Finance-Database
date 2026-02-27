# database/schema.py

from sqlite3 import Connection
from database.connection import get_connection


def initialize_schema(connection: Connection) -> None:
    connection.executescript("""
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        institution TEXT,
        type TEXT NOT NULL,
        number TEXT NOT NULL DEFAULT '0000',
        is_active INTEGER NOT NULL DEFAULT 1
    );

    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES categories(id)
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date_added DATE NOT NULL DEFAULT (DATE('now')),
        date_modified DATE NOT NULL DEFAULT (DATE('now')),
        source TEXT,
        account_id INTEGER NOT NULL,
        transaction_date DATE NOT NULL,
        post_date DATE,
        description TEXT,
        amount REAL NOT NULL,
        category_id INTEGER,
        cleared INTEGER NOT NULL DEFAULT 0,
        verified_receipt INTEGER NOT NULL DEFAULT 0,
        verified_statement INTEGER NOT NULL DEFAULT 0,
        comment TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );
    """)
