# myapp/cli.py

import argparse
import logging
import os 
from dotenv import load_dotenv
from myapp import author_api, db

# Load environment variables from a .env file in the project root
load_dotenv()

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command-line arguments and return the parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Retrieve the OpenLibrary JSON profile for a given author name."
    )
    parser.add_argument("author", type=str, help="The name of the author to search for.")
    return parser.parse_args()

def main():
    args = parse_args()
    logger.info(f"Searching for author: {args.author}")

    author_key, author_data = author_api.search_author(args.author)
    logger.info(f"Found author key: {author_key}")
    logger.debug("Author JSON profile: %s", author_data)

    # Get the database file from an environment variable (default: "authors.db")
    db_file = os.environ.get("DATABASE_FILE", "authors.db")
    conn = db.create_connection()
    if conn is None:
        logger.error("Failed to connect to the database.")
        return
    db.create_tables(conn)

    # Insert the author data into the tables
    db.insert_author(conn, author_data)
    db.insert_ratings(conn, author_data)
    conn.close()
    
    logger.info("Author data successfully stored in the database.")

if __name__ == '__main__':
    main()
