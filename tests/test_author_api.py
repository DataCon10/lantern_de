# tests/test_author_api.py

import sys
import os

# Add project root to sys.path so we can import "myapp"

from myapp import author_api

def test_search_author_valid():
    # Given a known author name; note this test uses real API calls.
    author_name = "J.K. Rowling"
    author_key, author_data = author_api.search_author(author_name)
    
    # Check that the author_key is a non-empty string and starts with "OL"
    assert isinstance(author_key, str)
    assert author_key.startswith("OL")
    
    # Check that the returned data includes the expected name substring
    assert "rowling" in author_data.get("name", "").lower()
