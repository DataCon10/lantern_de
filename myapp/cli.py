# myapp/cli.py

import argparse
from myapp import author_api

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
    print(f"Searching for author: {args.author}")

    author_key, author_data = author_api.search_author(args.author)
    print(f"Found author key: {author_key}")
    print("\nAuthor JSON profile:")
    print(author_data)

if __name__ == '__main__':
    main()
