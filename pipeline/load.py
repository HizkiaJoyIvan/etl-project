from sqlalchemy import create_engine
import pandas as pd
import os

def load_to_postgresql(df):
    db = os.getenv("DATABASE_URL")
    engine = create_engine(db)
    conn = engine.raw_connection()


    print("Connected to Database successfully")

    try:
        with engine.connect() as conn:
            df.to_sql("transformed_datas", conn, index=False, if_exists='append')

    except Exception as e:
        print(f"Error: {e}")

