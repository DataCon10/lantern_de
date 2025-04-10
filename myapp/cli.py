import argparse
import logging
import os
from pprint import pformat
from dotenv import load_dotenv
from myapp import author_api, db, dashboard
from myapp.logging_config import configure_logging

# Load environment variables from the .env file located in the project root.
load_dotenv()

# Configure logging using centralized configuration.
configure_logging()
logger = logging.getLogger(__name__)

def parse_args():
    """
    Parse command-line arguments and return the parsed arguments with subcommands.
    """
    parser = argparse.ArgumentParser(
        description="IMDb for Authors CLI Tool."
    )
    subparsers = parser.add_subparsers(dest="command", required=True,
                                       help="Sub-commands: 'run' to fetch and store data, 'dashboard' to launch the interactive dashboard.")

    # Subcommand: run (fetch and store author data)
    run_parser = subparsers.add_parser("run", help="Fetch author data from OpenLibrary and store it in the database.")
    run_parser.add_argument("author", type=str, help="The name of the author to search for.")

    # Subcommand: dashboard (launch interactive dashboard for a given author key)
    dash_parser = subparsers.add_parser("dashboard", help="Launch the interactive dashboard for a given author.")
    dash_parser.add_argument("--author-key", type=str, default="OL23919A",
                             help="The author key to display on the dashboard (default: OL23919A).")
    return parser.parse_args()

def main():
    args = parse_args()
    if args.command == "run":
        logger.info("Running author fetch and store process for: %s", args.author)

        try:
            author_key, author_data = author_api.search_author(args.author)
            logger.info("Found author key: %s", author_key)
            logger.debug("Author JSON profile:\n%s", pformat(author_data))
        except Exception as e:
            logger.exception("Error fetching author data: %s", e)
            return

        # Create a Database instance and perform operations.
        database = db.Database()
        try:
            conn = database.connect()
            if conn is None:
                logger.error("Failed to connect to the database.")
                return

            database.create_tables()
            database.insert_author(author_data)
            database.insert_ratings(author_data)
            logger.info("Author data successfully stored in the database.")
        except Exception as e:
            logger.exception("An error occurred during database operations: %s", e)
        finally:
            if database:
                database.close()

    elif args.command == "dashboard":
        logger.info("Launching interactive dashboard for author key: %s", args.author_key)
        db_file = os.environ.get("DATABASE_FILE", "authors.db")
        dashboard.run_dashboard(args.author_key, db_file)

if __name__ == '__main__':
    main()
