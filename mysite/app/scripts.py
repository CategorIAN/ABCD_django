import re
from django.db import connection


def find_null_bytes():
    with connection.cursor() as cursor:
        # Get the list of all tables
        cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            print(f"Checking table: {table_name}")

            # Get the list of columns in the table
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{table_name}';")
            columns = cursor.fetchall()

            for column in columns:
                column_name = column[0]
                try:
                    # Check for null byte in this column
                    query = f"SELECT * FROM {table_name} WHERE {column_name}::text LIKE '%\\x00%'"
                    cursor.execute(query)
                    results = cursor.fetchall()

                    if results:
                        print(f"Null byte found in table '{table_name}', column '{column_name}':")
                        for result in results:
                            print(result)
                except Exception as e:
                    # Skip if there's an issue with the column (e.g., unsupported data type for LIKE)
                    print(f"Error querying table '{table_name}', column '{column_name}': {e}")

