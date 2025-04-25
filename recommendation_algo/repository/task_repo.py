import sqlite3
import pandas as pd

import os

# на вершине модуля
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB_PATH = os.path.join(BASE_DIR, "your_database.db")



def get_completed_task_ids(student_id: int) -> list[int]:
    """
    Возвращает список ID задач, которые уже решал студент.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT DISTINCT T.id
        FROM Tasks T
        JOIN Lesson_tasks LT ON T.id = LT.task_id
        JOIN Lessons L ON LT.lesson_id = L.id
        JOIN Schedule_lessons SL ON L.id = SL.lesson_id
        JOIN Schedule S ON SL.schedule_id = S.id
        WHERE S.student_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(student_id,))
    conn.close()
    return df["id"].tolist()


def get_tasks_with_themes() -> pd.DataFrame:
    """
    Возвращает все задачи с привязкой к темам, включая section_id.
    """
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT T.id, T.section_id, T.description, T.complexity, T.theme_id, TH.name as theme_name
        FROM Tasks T
        JOIN Themes TH ON T.theme_id = TH.id
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_tasks_by_student_and_block(student_id: int, block_id: int) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT T.id, T.description, T.theme_id, TH.name as theme_name,
               T.complexity, LT.grade
        FROM Tasks T
        JOIN Lesson_tasks LT ON T.id = LT.task_id
        JOIN Lessons L ON LT.lesson_id = L.id
        JOIN Themes TH ON T.theme_id = TH.id
        JOIN Schedule_lessons SL ON L.id = SL.lesson_id
        JOIN Schedule S ON SL.schedule_id = S.id
        WHERE S.student_id = ?
          AND L.section_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(student_id, block_id))
    conn.close()

    # 🔍 Отладочный вывод
    print(f"📥 SQL result for student_id={student_id}, block_id={block_id}: {len(df)} rows")

    return df



def get_tasks_by_themes(theme_ids: list[int]) -> pd.DataFrame:
    """
    Возвращает все задачи по указанным темам.
    """
    if not theme_ids:
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    placeholder = ','.join(['?'] * len(theme_ids))
    query = f"""
        SELECT T.id, T.description, T.theme_id, TH.name as theme_name, T.complexity
        FROM Tasks T
        JOIN Themes TH ON T.theme_id = TH.id
        WHERE T.theme_id IN ({placeholder})
    """
    df = pd.read_sql_query(query, conn, params=theme_ids)
    conn.close()
    return df
