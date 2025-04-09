import argparse
import certifi
import requests
import sys

def parse_args():
    parser = argparse.ArgumentParser(description="Retrieve the OpenLibrary JSON profile for a given author name.")
    parser.add_argument("author", type=str, help="The name of the author to search for.")
    return parser.parse_args()

def search_author(author_name):
    """Search for the author on OpenLibrary and return the first result's key and JSON document."""
    url = f"https://openlibrary.org/search/authors.json?q=j%20k%20rowling"
    try:
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during the API call: {e}")
        sys.exit(1)

    data = response.json()
    if data.get("numFound", 0) == 0 or not data.get("docs"):
        print("No author found for the given name.")
        sys.exit(1)

    # Return the first result's key and the document
    first_author = data["docs"][0]
    author_key = first_author["key"].replace("/authors/", "")
    return author_key, first_author

def main():
    args = parse_args()
    print(f"Searching for author: {args.author}")

    author_key, author_data = search_author(args.author)
    print(f"Found author key: {author_key}")
    print("\nAuthor JSON profile:")
    print(author_data)

if __name__ == '__main__':
    main()
