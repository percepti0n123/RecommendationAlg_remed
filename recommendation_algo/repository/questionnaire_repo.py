# recommendation_algo/repository/questionnaire_repo.py

import sqlite3
import pandas as pd
from db.db import DB_PATH

def get_questionnaire(student_id: int) -> pd.DataFrame:
    """
    Возвращает строку из Questionnaire для заданного студента.
    Если анкета не найдена, вернёт пустой DataFrame.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(
            "SELECT * FROM Questionnaire WHERE student_id = ?",
            conn,
            params=(student_id,)
        )
    finally:
        conn.close()
    return df

def upsert_questionnaire(
    student_id: int,
    desired_score: int,
    weekly_hours: float,
    topic_preferences: str,
    start_date: str = None
) -> None:
    """
    Вставляет или обновляет запись в Questionnaire.
    topic_preferences — CSV строка (например, 'Векторы, Логарифмы').
    start_date в формате 'YYYY-MM-DD' или None.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Questionnaire(student_id, desired_score, weekly_hours, topic_preferences, start_date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(student_id) DO UPDATE SET
                desired_score=excluded.desired_score,
                weekly_hours=excluded.weekly_hours,
                topic_preferences=excluded.topic_preferences,
                start_date=excluded.start_date
            ;
        """, (student_id, desired_score, weekly_hours, topic_preferences, start_date))
        conn.commit()
    finally:
        conn.close()
