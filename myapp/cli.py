# myapp/cli.py

import argparse
import logging
import os
from pprint import pprint
from dotenv import load_dotenv
from myapp import author_api, db

# Load environment variables from the .env file located in the project root.
load_dotenv()

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
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
    logger.info("Searching for author: %s", args.author)

    # Retrieve the author profile from the API.
    author_key, author_data = author_api.search_author(args.author)
    logger.info("Found author key: %s", author_key)
    logger.debug("Author JSON profile: %s", author_data)

    # Create an instance of the Database class.
    database = db.Database()
    try:
        conn = database.connect()
        if conn is None:
            logger.error("Failed to connect to the database.")
            return

        # Create tables, insert data, etc.
        database.create_tables()
        database.insert_author(author_data)
        database.insert_ratings(author_data)
        logger.info("Author data successfully stored in the database.")

    except Exception as e:
        logger.exception("An error occurred during database operations: %s", e)

    finally:
        # Ensure the database connection is closed even if errors occur.
        if database:
            database.close()

if __name__ == '__main__':
    main()
