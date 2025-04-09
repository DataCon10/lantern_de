# myapp/author_api.py

import requests
import logging
from typing import Tuple, Dict, Any
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

class AuthorAPICallError(Exception):
    """Custom exception for API call failures."""
    pass

def search_author(author_name: str, verify_ssl: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    Search for the author on OpenLibrary and return the first result's key and JSON document.

    Args:
        author_name (str): The name of the author to search for.
        verify_ssl (bool): Flag for SSL verification (default is False as a temporary workaround).

    Returns:
        Tuple[str, Dict[str, Any]]: A tuple containing the author key and the author data.

    Raises:
        AuthorAPICallError: If the API call fails or no author is found.
    """
    # Build parameters for the request to ensure proper URL encoding.
    params = {"q": author_name}
    url = "https://openlibrary.org/search/authors.json"
    try:
        response = requests.get(url, params=params, timeout=10, verify=verify_ssl)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error("Error during the API call: %s", e)
        raise AuthorAPICallError(f"Error during API call: {e}") from e

    data = response.json()
    if data.get("numFound", 0) == 0 or not data.get("docs"):
        msg = f"No author found for the given name: {author_name}"
        logger.error(msg)
        raise AuthorAPICallError(msg)

    # Take the first result and remove the '/authors/' prefix from the key.
    first_author = data["docs"][0]
    author_key = first_author["key"].replace("/authors/", "")
    logger.info("Author found with key: %s", author_key)
    return author_key, first_author
