# IMDb for Authors

## Overview
"IMDb for Authors" is a command‐line tool and interactive dashboard that retrieves and stores an author's profile data from the OpenLibrary API. It provides both a text‐based interface for fetching and storing data and a web dashboard to visualise key metrics such as the author’s name, top book, average rating, and ratings count distribution. The application is designed to be reliable, flexible, and of high quality, with a robust modular architecture that is easy to execute and extend.

## Reliability
- **Robust Error Handling:**  
  The application uses custom exceptions and detailed logging to capture and handle errors gracefully during API calls and database operations.
  
- **Database Integrity:**  
  SQL queries and database management use best practices to ensure data integrity. 

- **Atomic Operations:**  
  Data insertion and updates are managed within controlled transactions, ensuring data consistency even when partial failures occur.

- **Testable Modules:**  
  The system is divided into modular components (API, database, dashboard, CLI) that can be individually tested and maintained.

## Flexibility
- **Configurable Settings:**  
  The application uses environment variables (loaded via a `.env` file) for key settings such as `LOG_LEVEL` and `DATABASE_FILE`. This externalises configuration and makes it easy to adjust the system for different environments without code changes.

- **Modular Architecture:**  
  Each component (e.g., `author_api`, `db`, `dashboard`, `cli`) is isolated and self-contained. This design allows for straightforward extensions like adding new features (e.g., detailed works or additional analytics) without impacting other modules.

- **Interactive Dashboard:**  
  Users can choose between a CLI mode for basic fetching and storage, and an interactive web dashboard (using Dash) that visualises author information and rating distributions.

## Quality of Information
- **Comprehensive Data Retrieval:**  
  The tool gathers multiple data points from the API, including the author’s name, top book, average rating, and detailed ratings counts. It selects the best matching record based on metrics like the number of user ratings.
- The tool additionally filters author records based on their highest number of ratings, ensuring the best quality author record is returned.

- **Real-Time Updates:**  
  Data is fetched directly from OpenLibrary, ensuring that information is current. The design is ready to accommodate further enrichments (such as author works) for greater depth.

- **Analytical Insights:**  
  In addition to storing raw data, the dashboard processes and presents key metrics in a clear manner—such as a summary of the author's profile and an interactive bar chart of the ratings count distribution.

## Amount of Information
- **Rich Data Points:**  
  The application retrieves and displays a variety of details:
  - Basic profile: Author name, top book.
  - Quality metrics: Average rating, ratings count (1-star through 5-star).
  - Engagement metrics (readership data) for potential future extension.
  
- **Scalable Data Model:**  
  Although the MVP focuses on author profiles and ratings, the design anticipates future expansion (e.g., adding an author’s works, reviews, or more granular statistics).

## How to Execute the Project
### Prerequisites
- **Python 3.8+** installed.
- Docker (optional) if you prefer containerisation.

### Setup
1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd your_project_root
