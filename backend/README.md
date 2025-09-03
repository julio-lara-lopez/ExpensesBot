
# Expenses Bot Backend

This is the backend for the Expenses Bot, a FastAPI application for managing personal expenses.

## About the Project

This project provides a simple yet powerful API for tracking expenses. It allows you to categorize your expenses, add keywords to categories for easier classification, and retrieve summaries of your spending. The backend is built with FastAPI and uses a SQLite database for data storage.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

*   Python 3.8 or higher
*   uv for dependency management

### Installation

1.  Clone the repo
    ```sh
    git clone https://your_repo_url/expenses-bot-backend.git
    ```
2.  Install dependencies
    ```sh
    uv sync
    ```
3.  Create a `.env` file and set the `DB_PATH` variable:
    ```
    DB_PATH=expenses.db
    ```
4.  Initialize the database:
    ```sh
    python init_db.py
    ```

### Running the Application

To run the application, use the following command:

```sh
uv run uvicorn src.main:app --reload && uv run python bot.py
```

The application will be available at `http://localhost:8000`.

## API Endpoints

The API is documented using Swagger UI, which is available at `http://localhost:8000/docs` when the application is running.

### Categories

*   **POST /categories**
    *   Adds a new category.
    *   **Body**:
        ```json
        {
          "name": "string",
          "emoji": "string"
        }
        ```
    *   **Response**:
        ```json
        {
          "status": "success",
          "message": "Category 'string' added."
        }
        ```

*   **DELETE /categories/{category_id}**
    *   Removes a category.
    *   **Response**:
        ```json
        {
          "status": "success",
          "message": "Category with id {category_id} removed."
        }
        ```

*   **GET /categories**
    *   Lists all categories.
    *   **Response**:
        ```json
        [
          {
            "id": 0,
            "name": "string",
            "emoji": "string"
          }
        ]
        ```

*   **GET /categories/{category_id}/keywords**
    *   Gets all keywords for a specific category.
    *   **Response**:
        ```json
        [
          "string"
        ]
        ```

*   **POST /categories/{category_id}/keywords**
    *   Adds a keyword to a category.
    *   **Body**:
        ```json
        {
          "keyword": "string"
        }
        ```
    *   **Response**:
        ```json
        {
          "status": "success",
          "message": "Keyword 'string' added to category {category_id}."
        }
        ```

*   **DELETE /categories/{category_id}/keywords**
    *   Removes a keyword from a category.
    *   **Body**:
        ```json
        {
          "keyword": "string"
        }
        ```
    *   **Response**:
        ```json
        {
          "status": "success",
          "message": "Keyword 'string' removed from category {category_id}."
        }
        ```

### Expenses

*   **GET /expenses**
    *   Lists expenses for a given period and user.
    *   **Query Parameters**:
        *   `period`: "today", "week", or "month" (defaults to "today")
        *   `user_id`: integer (defaults to 0)
    *   **Response**:
        ```json
        [
          {
            "category": "string",
            "amount": 0,
            "currency": "string",
            "note": "string",
            "ts_utc": "2025-09-02T12:00:00Z"
          }
        ]
        ```

*   **GET /expenses/summary**
    *   Gets a summary of expenses for a given period and user.
    *   **Query Parameters**:
        *   `period`: "today", "week", or "month" (defaults to "today")
        *   `user_id`: integer (defaults to 0)
    *   **Response**:
        ```json
        [
          {
            "currency": "string",
            "total": 0,
            "n": 0
          }
        ]
        ```

*   **POST /expenses**
    *   Adds a new expense.
    *   **Body**:
        ```json
        {
          "user_id": 0,
          "category_id": 0,
          "category_name": "string",
          "amount": 0,
          "currency": "string",
          "note": "string"
        }
        ```
    *   **Response**:
        ```json
        {
          "status": "success",
          "message": "Expense added."
        }
        ```
