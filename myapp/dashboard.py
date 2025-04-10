import dash
from dash import html, dcc
import sqlite3
import os
import pandas as pd
import logging
from typing import Dict, Any
import plotly.express as px

logger = logging.getLogger(__name__)

def fetch_author_info(author_key: str, db_file: str) -> Dict[str, Any]:
    """
    Fetch the author's name, top book, and average rating from the database.

    Args:
        author_key (str): The author key (e.g., "OL23919A").
        db_file (str): Path to the SQLite database file.

    Returns:
        Dict[str, Any]: Contains 'author_name', 'top_work', and 'avg_rating'. 
                        Defaults to placeholder values if data is missing.
    """
    try:
        with sqlite3.connect(db_file) as conn:
            cur = conn.cursor()
            cur.execute("SELECT name, top_work FROM authors WHERE author_id = ?", (author_key,))
            author_row = cur.fetchone()
            cur.execute("SELECT ratings_average FROM ratings WHERE author_id = ?", (author_key,))
            ratings_row = cur.fetchone()
    except sqlite3.Error as e:
        logger.error("Database error in fetch_author_info: %s", e)
        return {"author_name": "Error", "avg_rating": "Error", "top_work": "Error"}

    author_name, top_work = (author_row if author_row else ("Unknown Author", "No top book"))
    avg_rating = ratings_row[0] if ratings_row and ratings_row[0] is not None else None
    logger.info("Fetched info: author_name=%s, top_work=%s, avg_rating=%s", author_name, top_work, avg_rating)
    return {"author_name": author_name, "avg_rating": avg_rating, "top_work": top_work}

def fetch_ratings_counts(author_key: str, db_file: str) -> Dict[str, int]:
    """
    Fetch the counts of ratings (1-star to 5-star) for the given author.

    Args:
        author_key (str): The author key (e.g., "OL23919A").
        db_file (str): Path to the SQLite database file.

    Returns:
        Dict[str, int]: Keys "1-star", "2-star", "3-star", "4-star", "5-star".
                        Returns zeros if no record is found.
    """
    try:
        with sqlite3.connect(db_file) as conn:
            cur = conn.cursor()
            query = """
                SELECT ratings_count_1, ratings_count_2, ratings_count_3, 
                       ratings_count_4, ratings_count_5
                FROM ratings
                WHERE author_id = ?
            """
            cur.execute(query, (author_key,))
            row = cur.fetchone()
    except sqlite3.Error as e:
        logger.error("Database error in fetch_ratings_counts for author %s: %s", author_key, e)
        return {f"{i}-star": 0 for i in range(1, 6)}
    
    if row:
        counts = {f"{i}-star": count for i, count in zip(range(1, 6), row)}
        logger.info("Fetched ratings counts for author %s: %s", author_key, counts)
        return counts
    else:
        logger.warning("No ratings record found for author key %s", author_key)
        return {f"{i}-star": 0 for i in range(1, 6)}

def create_summary_layout(info: Dict[str, Any]) -> html.Div:
    """
    Build the summary layout displaying the author's name, top work, and average rating.
    
    Args:
        info (Dict[str, Any]): Dictionary containing 'author_name', 'top_work', and 'avg_rating'.
    
    Returns:
        html.Div: The HTML layout for the summary.
    """
    avg_rating = info.get("avg_rating")
    formatted_rating = f"{avg_rating:.2f}" if isinstance(avg_rating, (int, float)) else (avg_rating or "No rating")
    
    return html.Div(
        children=[
            html.H1("Author Profile", style={"textAlign": "center"}),
            html.Div(
                children=[
                    html.P(f"Author Name: {info.get('author_name')}", style={"fontSize": "24px"}),
                    html.P(f"Top Book: {info.get('top_work')}", style={"fontSize": "24px"}),
                    html.P(f"Average Rating: {formatted_rating}", style={"fontSize": "24px"})
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

def create_ratings_count_chart(rating_counts: Dict[str, int]) -> Dict[str, Any]:
    """
    Create a bar chart for the ratings count distribution using Plotly.

    Args:
        rating_counts (Dict[str, int]): A dictionary with keys "1-star" to "5-star".

    Returns:
        Dict[str, Any]: A Plotly figure dictionary for the bar chart.
    """
    data = [{"Rating": rating, "Count": count} for rating, count in rating_counts.items()]
    df = pd.DataFrame(data)
    fig = px.bar(
        df, x="Rating", y="Count",
        title="Ratings Count Distribution",
        labels={"Count": "Number of Ratings"}
    )
    return fig

def build_dashboard_layout(author_info: Dict[str, Any], rating_counts: Dict[str, int]) -> html.Div:
    """
    Build and return the complete dashboard layout with summary and ratings count chart.
    
    Args:
        author_info (Dict[str, Any]): Author's basic info.
        rating_counts (Dict[str, int]): Ratings counts dictionary.
    
    Returns:
        html.Div: The complete Dash layout.
    """
    summary_layout = create_summary_layout(author_info)
    chart_figure = create_ratings_count_chart(rating_counts)
    
    return html.Div(
        children=[
            summary_layout,
            html.Div(
                children=[dcc.Graph(id="ratings-count-chart", figure=chart_figure)],
                style={
                    "marginTop": "50px",
                    "maxWidth": "800px",
                    "marginLeft": "auto",
                    "marginRight": "auto"
                }
            )
        ]
    )

def run_dashboard(author_key: str, db_file: str) -> None:
    """
    Launch the Dash dashboard for the given author key.

    Args:
        author_key (str): The OpenLibrary author key (e.g., "OL23919A").
        db_file (str): The SQLite database file path.
    """
    author_info = fetch_author_info(author_key, db_file)
    rating_counts = fetch_ratings_counts(author_key, db_file)
    
    app = dash.Dash(__name__)
    app.title = "Author Profile Dashboard"
    app.layout = build_dashboard_layout(author_info, rating_counts)
    
    logger.info("Launching dashboard server for author key: %s", author_key)
    # Note: app.run is blocking; run with debug=True for easier development.
    app.run(debug=True)

if __name__ == '__main__':
    default_author_key = "OL23919A"
    default_db_file = os.environ.get("DATABASE_FILE", "authors.db")
    run_dashboard(default_author_key, default_db_file)
