import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy import text
from datetime import datetime

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
database_type = os.getenv("DATABASE_NAME").lower()

# Construct connection string based on database type
if database_type == "postgresql":
    # Ensure port is included only if provided
    port_str = f":{db_port}" if db_port else ":5432"
    conn_string = f"postgresql://{db_user}:{db_password}@{db_host}{port_str}/{db_name}"
elif database_type == "mysql":
    # MySQL uses mysql+mysqlconnector or other drivers
    port_str = f":{db_port}" if db_port else ":3306"
    # Example using mysql+mysqlconnector (ensure driver is installed: pip install mysql-connector-python)
    conn_string = (
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}{port_str}/{db_name}"
    )
# Add more database types here as needed (e.g., sqlserver, oracle)
else:
    raise ValueError(f"Unsupported database type: {database_type}")


engine = create_engine(conn_string)


def get_schema():
    metadata = MetaData()
    metadata.reflect(engine)
    result = []

    for table in metadata.tables.values():
        result.append(f"Table: {table.name}")
        result.append("Columns:")
        for column in table.columns:
            comment = getattr(column, "comment", None)
            comment_str = f": {comment}" if comment else ""
            result.append(f"  {column.name}: {column.type}{comment_str}")
        result.append("\n")

    return "\n".join(result)


# print(get_schema())


def execute_query(query: str) -> list[dict]:
    """
      Execute a query and return the result as a list of dictionaries.

      Args:
          query (string): the query to execute

    Returns:
        list: the result of the query as a list of dictionaries.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            keys = result.keys()  # Get column names
        return_res = []
        for row in result.fetchall():
            processed_row = []
            # Ensure row elements are accessed correctly (SQLAlchemy Row is tuple-like)
            row_tuple = tuple(row)
            for value in row_tuple:
                if isinstance(value, datetime):
                    # Format datetime objects as ISO 8601 strings with 'Z' for UTC timezone indication
                    # This assumes datetime objects are timezone-aware UTC or naive UTC.
                    # Adjust if database returns timezone-naive local times.
                    processed_row.append(value.isoformat() + "Z")
                elif value is None:
                    processed_row.append(None)  # Handle None explicitly
                else:
                    # Keep other types as they are, converting to string as a fallback
                    processed_row.append(str(value))
                # Create a dictionary for each row with processed values
                return_res.append(dict(zip(keys, processed_row)))
        return return_res
    except Exception as e:
        print(f"Error executing query: {e}")
        return [{"error": str(e)}]


# print(execute_query("SELECT * FROM merchant_entity LIMIT 10"))
