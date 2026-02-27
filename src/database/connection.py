# database/connection.py

import sqlite3
from const import root_dir

DB_PATH = root_dir / "data" / "finance.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn
