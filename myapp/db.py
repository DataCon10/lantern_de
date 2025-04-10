import sqlite3
import logging
import os
from typing import Any, Dict, Optional
from myapp import queries

logger = logging.getLogger(__name__)
DATABASE_FILE: str = os.environ.get("DATABASE_FILE", "authors.db")

class Database:
    def __init__(self, db_file: str = DATABASE_FILE) -> None:
        self.db_file: str = db_file
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> Optional[sqlite3.Connection]:
        """Establish and return a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_file)
            logger.info("Connected to database: %s", self.db_file)
        except sqlite3.Error as e:
            logger.error("Error connecting to database: %s", e)
            self.conn = None
        return self.conn

    def create_tables(self) -> None:
        """Create authors and ratings tables if they don't already exist."""
        if not self.conn:
            logger.error("No database connection available to create tables.")
            return
        try:
            cur = self.conn.cursor()
            cur.execute(queries.CREATE_AUTHORS_TABLE)
            cur.execute(queries.CREATE_RATINGS_TABLE)
            self.conn.commit()
            logger.info("Tables created successfully.")
        except sqlite3.Error as e:
            logger.error("Error creating tables: %s", e)
            self.conn.rollback()

    def insert_author(self, author: Dict[str, Any]) -> None:
        """Insert or update the author profile into the authors table."""
        if not self.conn:
            logger.error("Cannot insert author without a database connection.")
            return
        values = (
            author.get("key"),
            author.get("name"),
            author.get("birth_date"),
            author.get("top_work"),
            author.get("work_count"),
        )
        try:
            cur = self.conn.cursor()
            cur.execute(queries.INSERT_OR_REPLACE_AUTHOR, values)
            self.conn.commit()
            logger.info("Inserted/Updated author %s", author.get("key"))
        except sqlite3.Error as e:
            logger.error("Error inserting/updating author %s: %s", author.get("key"), e)
            self.conn.rollback()

    def insert_ratings(self, author: Dict[str, Any]) -> None:
        """Insert or update the ratings data in the ratings table."""
        if not self.conn:
            logger.error("Cannot insert ratings without a database connection.")
            return
        values = (
            author.get("key"),
            author.get("ratings_average"),
            author.get("ratings_count"),
            author.get("ratings_count_1", 0),
            author.get("ratings_count_2", 0),
            author.get("ratings_count_3", 0),
            author.get("ratings_count_4", 0),
            author.get("ratings_count_5", 0),
        )
        try:
            cur = self.conn.cursor()
            cur.execute(queries.INSERT_OR_REPLACE_RATINGS, values)
            self.conn.commit()
            logger.info("Inserted/Updated ratings for author %s", author.get("key"))
        except sqlite3.Error as e:
            logger.error("Error inserting/updating ratings for author %s: %s", author.get("key"), e)
            self.conn.rollback()

    def close(self) -> None:
        """Close the database connection if it exists."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed.")
