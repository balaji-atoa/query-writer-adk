![data-retriever.png](<https://media-hosting.imagekit.io/142d3806d4b942b0/data-retriever.png?Expires=1840266918&Key-Pair-Id=K2ZIVPTIP2VGHC&Signature=OHjaC6ZVGr5ox8Ek2yx9wzPnHKeaQEBdeoOEgrsYgzvCCuVQ4tLSSsW8BK5NZlUXKMmGdXumu4z--lV0-GFLgN3tFtf3UZilKLQ8oVxIxhugnZz376zxrEOANx1N1yhUsfCr38Tabpn9gcu5LfAKed-aBJHPbsPmOWGluB82jBYXfFcZR27yqUPcodE8922TZcsQ~wIeLl6gVvL68cZ~4xPXdhiWwVGBCGjHZSWx7S8gbphzfuh06XEzklB91oQeq5aemeKmqJKaWoxGgHW1gL8dBh4uMeqGOZr475zWyCwLb9BtB9lQZ2c6dt4i~Sd3Eaa5~qGH7MQzJm9405JdVA__>)

## Overview

This project implements an AI agent named "Adam" using the Google Agent Development Kit (ADK) (`google-adk`). Adam is designed as an expert database engineer specializing in generating efficient and correct SQL queries for various database systems based on user instructions and a provided database schema.

The agent dynamically adapts its query generation based on the target database specified (e.g., PostgreSQL, MySQL, SQL Server, Oracle) and utilizes database-specific syntax and conventions.

## Features

*   **Natural Language to SQL:** Converts user instructions into SQL queries.
*   **Schema-Aware:** Uses the provided database schema (`get_schema()`) to generate accurate queries.
*   **Multi-Database Support:** Dynamically generates connection strings and tailors SQL syntax for different database types (currently supports PostgreSQL and MySQL, with placeholders for SQL Server and Oracle). Requires appropriate DBAPI drivers to be installed (e.g., `psycopg2` for PostgreSQL, `mysql-connector-python` for MySQL, `pyodbc` for SQL Server, `oracledb` for Oracle).
*   **Query Execution:** Includes a tool (`execute_query`) to run the generated SQL query against the target database and return results.
*   **Result Formatting:** Query results are returned as a list of dictionaries, with datetime objects converted to ISO 8601 strings.

## Prerequisites

*   Python 3.10+
*   Required Python libraries (see `requirements.txt`)
*   Access to a target database (PostgreSQL, MySQL, etc.)
*   Appropriate DBAPI driver installed for the target database (e.g., `psycopg2`, `mysql-connector-python`, `pyodbc`, `oracledb`).

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd sql-retriever # Or your project directory name
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate # Linux/macOS
    # .venv\Scripts\activate # Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # Install the DBAPI driver for your target database, e.g.:
    # pip install psycopg2-binary # For PostgreSQL
    # pip install mysql-connector-python # For MySQL
    # pip install pyodbc # For SQL Server
    # pip install oracledb # For Oracle
    ```

## Linting and Formatting

This project uses [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

**VS Code Integration:**

1.  Install the [Ruff VS Code extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff).
2.  Enable format on save (optional but recommended) in your VS Code settings (`settings.json`):
    ```json
    {
      "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
      },
      "editor.codeActionsOnSave": {
        "source.fixAll": "explicit"
      }
    }
    ```

**Manual Usage:**

*   Check for linting errors:
    ```bash
    ruff check .
    ```
*   Format files:
    ```bash
    ruff format .
    ```
*   Check for errors and automatically fix them (where possible):
    ```bash
    ruff check . --fix
    ```

## Configuration

The agent requires database connection details. The recommended way to provide these is using a `.env` file in the project root directory.

Create a file named `.env` with the following variables:

```dotenv
# --- Database Configuration ---
# Required:
DATABASE_NAME="postgresql" # e.g., postgresql, mysql, sqlserver, oracle (case-insensitive)
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_HOST="localhost" # Or your database host
DB_NAME="your_db_name"

**Optional / Database-Specific:**
*   `DB_PORT`: Database port (defaults used if not set: PostgreSQL=5432, MySQL=3306, Oracle=1521).

# --- ADK / LLM Configuration (If using Vertex AI) ---
# GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
# GOOGLE_CLOUD_LOCATION="your-gcp-location" # e.g., us-central1
# GOOGLE_GENAI_USE_VERTEXAI="True"
```

**Note:** Fill in the actual values for your database connection. Uncomment and set optional/database-specific variables as needed for your setup (SQL Server, Oracle).

If you are using Gemini via Vertex AI, ensure the `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `GOOGLE_GENAI_USE_VERTEXAI` variables are also set.

## Usage

The main agent entry point is `agent.agent`. You can interact with the agent using the ADK command-line tools.

**Ensure your virtual environment is activated and you are in the project root directory.**

1.  **Run with ADK CLI:**
    Interact with the agent directly in your terminal:
    ```bash
    adk run agent
    ```
    Then, type your instructions, for example:
    `> Show me the first 5 customers from the customers table`

2.  **Run with ADK Web UI (for local development):**
    Launch the ADK web interface for a chat-like experience:
    ```bash
    adk web
    ```
    Open the provided URL (usually `http://localhost:8000`) in your browser. Select the `agent` and start interacting.

**Example Interaction (CLI):**

```bash
$ adk run agent
Starting agent agent...
Agent agent started.
> Give me the names and email addresses of all users in the 'users' table
# Agent processes the request, generates SQL, executes it, and returns the result...
# (Output containing the SQL query, explanation, and results table)
>
```

The agent uses `agent.utils.db.get_schema()` to fetch the schema and `agent.utils.db.execute_query()` to run the generated queries against the configured database.

## Project Structure

```
.
├── agent/
│   ├── utils/
│   │   ├── db.py         # Database connection, schema retrieval, query execution
│   │   └── __init__.py
│   ├── agent.py        # Main agent definition (Adam)
│   └── __init__.py
├── .venv/              # Virtual environment (optional)
├── .gitignore
├── requirements.txt    # Project dependencies
├── .env                # Environment variables (Create this file)
└── README.md           # This file
```

## Contributing

Contributions are welcome! Please feel free to open an issue on the repository for bug reports or feature requests.

If you'd like to contribute code:

1.  Fork the repository.
2.  Create a new branch for your feature or bug fix.
3.  Make your changes.
4.  Ensure your code adheres to standard Python practices.
5.  Submit a pull request with a clear description of your changes.