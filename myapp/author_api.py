# myapp/author_api.py

import requests
import logging
from typing import Tuple, List, Dict, Any
import sys

logger = logging.getLogger(__name__)

class AuthorAPICallError(Exception):
    """Custom exception for API call failures."""
    pass

def select_best_author(docs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Select the best (most accurate) author record from the list of candidate documents.
    
    In this implementation, we choose the record with the highest 'ratings_count'.
    
    Assumption:
      We assume that the ratings_count (i.e. the total number of ratings submitted by users)
      is a better indicator of the record's completeness and popularity than work_count. A higher 
      ratings_count suggests that more users have provided feedback on the author's works, implying 
      that the record is more robust and well-maintained.

    #TODO: 
        - Verify Assumption using sample of authors.
    
    Args:
      docs (List[Dict[str, Any]]): List of author records from the API response.
      
    Returns:
      Dict[str, Any]: The selected author record.
      
    Raises:
      ValueError: If the list is empty.
    """
    if not docs:
        raise ValueError("No author records provided.")
    
    # Use ratings_count as the key for selection.
    best = max(docs, key=lambda doc: doc.get("ratings_count", 0))
    return best

def search_author(author_name: str, verify_ssl: bool = False) -> Tuple[str, Dict[str, Any]]:
    """
    Search for the author on OpenLibrary and return the best match's key and JSON document.
    Uses verify=False as a temporary workaround for SSL verification.
    
    Args:
      author_name (str): The name of the author to search for.
      verify_ssl (bool): Whether to verify SSL certificates (default is False).
      
    Returns:
      Tuple[str, Dict[str, Any]]: A tuple containing the author's key and the chosen author record.
      
    Raises:
      AuthorAPICallError: If the API call fails or no author is found.
    """
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
    
    docs = data["docs"]
    best_record = select_best_author(docs)
    author_key = best_record["key"].replace("/authors/", "")
    logger.info("Selected best author record with key: %s (ratings_count: %s)", 
                author_key, best_record.get("ratings_count"))
    return author_key, best_record
