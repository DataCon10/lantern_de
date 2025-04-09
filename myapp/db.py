# myapp/db.py

import sqlite3

DATABASE_FILE = "authors.db"

def create_connection(db_file=DATABASE_FILE):
    """Create and return a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error: {e}")
        return None

def create_tables(conn):
    """Create the authors and ratings tables if they don't already exist."""
    create_authors_table = """
    CREATE TABLE IF NOT EXISTS authors (
        author_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        birth_date TEXT,
        top_work TEXT,
        work_count INTEGER
    );
    """
    
    create_ratings_table = """
    CREATE TABLE IF NOT EXISTS ratings (
        author_id TEXT PRIMARY KEY,
        ratings_average REAL,
        ratings_count INTEGER,
        ratings_count_1 INTEGER,
        ratings_count_2 INTEGER,
        ratings_count_3 INTEGER,
        ratings_count_4 INTEGER,
        ratings_count_5 INTEGER,
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
    );
    """
    
    cur = conn.cursor()
    cur.execute(create_authors_table)
    cur.execute(create_ratings_table)
    conn.commit()
    print("Tables created successfully.")

def insert_author(conn, author):
    """Insert or update the core author profile into the authors table."""
    sql = """
    INSERT OR REPLACE INTO authors (author_id, name, birth_date, top_work, work_count)
    VALUES (?, ?, ?, ?, ?);
    """
    values = (
        author.get("key"),
        author.get("name"),
        author.get("birth_date"),
        author.get("top_work"),
        author.get("work_count"),
    )
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()

def insert_ratings(conn, author):
    """Insert or update the ratings data in the ratings table."""
    sql = """
    INSERT OR REPLACE INTO ratings (
        author_id,
        ratings_average,
        ratings_count,
        ratings_count_1,
        ratings_count_2,
        ratings_count_3,
        ratings_count_4,
        ratings_count_5
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
    """
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
    cur = conn.cursor()
    cur.execute(sql, values)
    conn.commit()
