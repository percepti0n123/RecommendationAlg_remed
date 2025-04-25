# repository/section_repo.py
import sqlite3
import pandas as pd
from db.db import DB_PATH

def get_sections() -> pd.DataFrame:
    """Получить все секции с их описаниями."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT id, description FROM Section"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df
