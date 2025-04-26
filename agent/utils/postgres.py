import os
from sqlalchemy import MetaData, create_engine
from sqlalchemy import text
from datetime import datetime

db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

conn_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(conn_string)


def get_schema():
    metadata = MetaData()
    metadata.reflect(engine)
    result = []

    for table in metadata.tables.values():
        result.append(f"Table: {table.name}")
        result.append("Columns:")
        for column in table.columns:
            result.append(f"  {column.name}: {column.type}: {column.comment}")
        result.append("\n")

    return "\n".join(result)


# print(get_schema())


def execute_query(query: str) -> list[dict]:
    """
      Execute a query and return the result as a list of dictionaries. Construct a table from the result.

      Args:
          query (string): the query to execute

    Returns:
        list: the result of the query
    """
    with engine.connect() as conn:
        result = conn.execute(text(query))
        keys = result.keys()  # Get column names
        return_res = []
        for row in result.fetchall():
            processed_row = []
            for value in row:
                if isinstance(value, datetime):
                    # Format datetime objects as ISO 8601 strings with 'Z' for UTC timezone indication
                    processed_row.append(value.isoformat() + "Z")
                else:
                    # Keep other types as they are (assuming they are JSON serializable)
                    processed_row.append(str(value))
            # Create a dictionary for each row with processed values
            return_res.append(dict(zip(keys, processed_row)))
    return return_res


# print(execute_query("SELECT * FROM merchant_entity LIMIT 10"))
