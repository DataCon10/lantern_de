# myapp/author_api.py

import requests
import sys

def search_author(author_name):
    """
    Search for the author on OpenLibrary and return the first result's key and JSON document.
    Uses verify=False as a temporary workaround for SSL verification.
    """
    # Build the URL using the provided author_name (URL-encoding can be added as needed)
    url = f"https://openlibrary.org/search/authors.json?q={author_name}"
    try:
        # Using verify=False temporarily due to certificate issues
        response = requests.get(url, timeout=10, verify=False)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error during the API call: {e}")
        sys.exit(1)

    data = response.json()
    if data.get("numFound", 0) == 0 or not data.get("docs"):
        print("No author found for the given name.")
        sys.exit(1)

    # Take the first result and clean up the key
    first_author = data["docs"][0]
    author_key = first_author["key"].replace("/authors/", "")
    return author_key, first_author
