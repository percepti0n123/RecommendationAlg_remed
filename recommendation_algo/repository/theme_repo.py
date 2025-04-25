# repository/theme_repo.py
import sqlite3
import pandas as pd
from db.db import DB_PATH

def get_student_theme_progress(student_id: int) -> pd.DataFrame:
    """Получить прогресс студента по темам."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT T.id as theme_id, T.section_id, STP.progress
        FROM Themes T
        LEFT JOIN StudentThemeProgress STP
        ON T.id = STP.theme_id AND STP.student_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(student_id,))
    conn.close()
    return df

def get_universal_plan(course_id: int) -> pd.DataFrame:
    """Получить универсальный план курса (очередность блоков)."""
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT section_id, priority
        FROM UniversalPlan
        WHERE course_id = ?
        ORDER BY priority
    """
    df = pd.read_sql_query(query, conn, params=(course_id,))
    conn.close()
    return df
