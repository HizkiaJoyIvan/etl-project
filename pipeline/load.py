from sqlalchemy import create_engine
import pandas as pd
import os

def load_to_postgresql():
    db = os.getenv("DATABASE_URL")
    engine = create_engine(db)
    