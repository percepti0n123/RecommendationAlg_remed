# recommendation_algo/repository/plan_repo.py

import sqlite3
import pandas as pd
from db.db import DB_PATH

def get_universal_plan(course_id: int) -> pd.DataFrame:
    """
    Возвращает для курса отсортированный по order_num список section_id.
    Колонки: section_id, order_num.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            """
            SELECT section_id, order_num
            FROM UniversalPlan
            WHERE course_id = ?
            ORDER BY order_num
            """,
            conn,
            params=(course_id,)
        )
    finally:
        conn.close()
    return df

def save_personal_plan(student_id: int, plan_json: str) -> None:
    """
    (Опционально) сохраняет сформированный JSON-план в отдельную таблицу.
    Таблица PersonalPlan(student_id, plan_json).
    Если её нет — можно создать аналогично Questionnaire.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PersonalPlan (
                student_id INTEGER PRIMARY KEY,
                plan_json TEXT NOT NULL,
                FOREIGN KEY(student_id) REFERENCES Students(id)
            );
        """)
        cursor.execute("""
            INSERT INTO PersonalPlan(student_id, plan_json)
            VALUES (?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                plan_json = excluded.plan_json
            ;
        """, (student_id, plan_json))
        conn.commit()
    finally:
        conn.close()
