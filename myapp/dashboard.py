# myapp/dashboard.py

import dash
from dash import html, dcc
import sqlite3
import os
import pandas as pd
import logging
from typing import Dict

logger = logging.getLogger(__name__)

def fetch_author_info(author_key: str, db_file: str) -> Dict[str, str]:
    """
    Fetch the author's name and average rating from the database.
    
    Args:
        author_key (str): The author key (e.g., "OL23919A").
        db_file (str): Path to the SQLite database file.
        
    Returns:
        dict: A dictionary with keys 'author_name' and 'avg_rating'.
              Returns default values if no data is found.
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        # Query the authors table to get the author name.
        cur.execute("SELECT name FROM authors WHERE author_id = ?", (author_key,))
        author_row = cur.fetchone()
        # Query the ratings table for the average rating.
        cur.execute("SELECT ratings_average FROM ratings WHERE author_id = ?", (author_key,))
        ratings_row = cur.fetchone()
        author_name = author_row[0] if author_row else "Unknown Author"
        avg_rating = ratings_row[0] if ratings_row else None
        logger.info("Fetched info: author_name=%s, avg_rating=%s", author_name, avg_rating)
        return {"author_name": author_name, "avg_rating": avg_rating}
    except Exception as e:
        logger.error("Error fetching author info: %s", e)
        return {"author_name": "Error", "avg_rating": "Error"}
    finally:
        if conn:
            conn.close()

def build_layout(info: Dict[str, str]) -> html.Div:
    """
    Build and return the dashboard layout using the fetched author info.
    
    Args:
        info (dict): Dictionary containing author info with keys 'author_name' and 'avg_rating'.
    
    Returns:
        html.Div: The main layout Div for the Dash app.
    """
    # Format the average rating to 2 decimal places if it is numeric.
    avg_rating = info.get("avg_rating")
    if isinstance(avg_rating, (int, float)):
        formatted_rating = f"{avg_rating:.2f}"
    else:
        formatted_rating = avg_rating or "No rating"
        
    return html.Div(
        children=[
            html.H1("Author Profile", style={"textAlign": "center"}),
            html.Div(
                children=[
                    html.P(f"Author Name: {info['author_name']}", style={"fontSize": "24px"}),
                    html.P(f"Average Rating: {formatted_rating}", style={"fontSize": "24px"}),
                ],
                style={
                    "margin": "auto",
                    "padding": "20px",
                    "border": "2px solid #ccc",
                    "borderRadius": "10px",
                    "maxWidth": "500px",
                    "textAlign": "center",
                    "backgroundColor": "#f9f9f9"
                }
            )
        ],
        style={"marginTop": "50px"}
    )

def run_dashboard(author_key: str, db_file: str):
    """
    Launch a simple interactive dashboard displaying the author's name and average rating.
    
    Args:
        author_key (str): The OpenLibrary author key.
        db_file (str): The SQLite database file path.
    """
    info = fetch_author_info(author_key, db_file)
    
    app = dash.Dash(__name__)
    app.title = "Author Profile Dashboard"
    
    app.layout = build_layout(info)
    
    logger.info("Launching dashboard server for author key: %s", author_key)
    # Start the Dash server.
    app.run(debug=True)

if __name__ == '__main__':
    # For standalone testing; defaults can be overridden by environment variables.
    default_author_key = "OL23919A"
    default_db_file = os.environ.get("DATABASE_FILE", "authors.db")
    run_dashboard(default_author_key, default_db_file)
