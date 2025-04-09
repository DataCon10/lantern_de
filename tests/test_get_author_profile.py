import sys
import requests
import json
from myapp import invoker

def test_search_author_returns_valid_key():
    # For testing purposes, use a known author.
    # The test assumes that "J.K. Rowling" exists.
    author_name = "J.K. Rowling"
    author_key, author_data = invoker.search_author(author_name)
    
    # Assert that we got a valid key (for example, it should start with "OL")
    assert isinstance(author_key, str), "Expected a string for author key."
    assert author_key.startswith("OL"), "Author key should start with 'OL'."
    
    # Also, verify that the returned data contains the correct name.
    expected_name = "J. K. Rowling"
    # Depending on how the API returns it, check using lower-case comparison.
    assert expected_name.lower() in author_data.get("name", "").lower(), "Author name does not match."
