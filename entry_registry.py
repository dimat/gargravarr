import os
import sqlite3


class EntryRegistry:
    def __init__(self, directory):
        self.directory = directory
        self.conn = self.connect_to_db()

    def connect_to_db(self):
        db_file = os.path.join(self.directory, 'rss_db.sqlite')
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
                id TEXT,
                source TEXT,
                PRIMARY KEY (id, source)
            )
        """)
        return conn

    def check_entry_exists(self, id, source):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 1 FROM entries WHERE id = ? AND source = ?
        """, (id, source))
        return cursor.fetchone() is not None

    def store_entry(self, id, source):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO entries (id, source) VALUES (?, ?)
        """, (id, source))
        self.conn.commit()
