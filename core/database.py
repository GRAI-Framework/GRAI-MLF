# gracie/core/database.py
import sqlite3
from typing import List, Optional
from ..models.topic import Topic

class DatabaseManager:
    """Manages SQLite database operations"""
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._initialize_db()
        
    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS topics (
                    id TEXT PRIMARY KEY,
                    name TEXT UNIQUE,
                    definition TEXT,
                    facts TEXT,
                    confidence REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            # Add other necessary tables
            
    def store_topic(self, topic: Topic) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO topics (id, name, definition, facts, confidence) VALUES (?, ?, ?, ?, ?)",
                    (topic.id, topic.name, topic.definition, str(topic.facts), topic.confidence)
                )
                return True
        except Exception:
            return False
