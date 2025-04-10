# SQL queries for the application

CREATE_AUTHORS_TABLE = """
CREATE TABLE IF NOT EXISTS authors (
    author_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT,
    top_work TEXT,
    work_count INTEGER
);
"""

CREATE_RATINGS_TABLE = """
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

INSERT_OR_REPLACE_AUTHOR = """
INSERT OR REPLACE INTO authors (author_id, name, birth_date, top_work, work_count)
VALUES (?, ?, ?, ?, ?);
"""

INSERT_OR_REPLACE_RATINGS = """
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

# Query to fetch the basic author info from the "authors" table.
SELECT_AUTHOR_INFO: str = """
SELECT name, top_work FROM authors WHERE author_id = ?
"""

# Query to fetch the average rating from the "ratings" table.
SELECT_AUTHOR_RATING: str = """
SELECT ratings_average FROM ratings WHERE author_id = ?
"""

# Query to fetch the individual rating counts from the "ratings" table.
SELECT_RATING_COUNTS: str = """
SELECT ratings_count_1, ratings_count_2, ratings_count_3, 
       ratings_count_4, ratings_count_5 
FROM ratings
WHERE author_id = ?
"""