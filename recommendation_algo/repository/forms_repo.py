# repository/forms_repo.py
import pandas as pd
from db.db import get_connection

def get_student_preferences(student_id):
    with get_connection() as conn:
        query = f"SELECT preferences FROM Forms WHERE student_id = {student_id}"
        df = pd.read_sql_query(query, conn)
        return df['preferences'].iloc[0].split(', ') if not df.empty else []

# recommendation_algo/repository/forms_repo.py
import sqlite3
import pandas as pd
from db.db import DB_PATH

def get_student_form(student_id):
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM Forms WHERE student_id = ?"
    form = pd.read_sql_query(query, conn, params=(student_id,))
    conn.close()
    return form
