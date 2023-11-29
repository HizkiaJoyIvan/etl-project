from sqlalchemy import create_engine
import pandas as pd
import os

def load_to_postgresql(df):
    db = os.getenv("DATABASE_URL")
    engine = create_engine(db)
    table_query = """
        CREATE TABLE transformed_data (
            name VARCHAR(255),
            duration FLOAT,
            popularity INTEGER,
            popularity_category VARCHAR(255),
            query VARCHAR(255),
            lowest_value INTEGER,
            lowest_value_date_range VARCHAR(255),
            highest_value INTEGER,
            highest_value_date_range VARCHAR(255)
        );
        """
    engine.execute(table_query)
    print("Connected to Database successfully")

    try:
        df.to_sql("transformed_data", engine, index=False, if_exists='append')
    except Exception as e:
        print(f"Error: {e}")

