# dev/inspect_db_schema.py

import sqlite3
import pandas as pd
from db.db import DB_PATH  # путь к your_database.db

def main():
    # Подключаемся к базе
    conn = sqlite3.connect(DB_PATH)
    try:
        # Читаем названия всех таблиц
        tables_df = pd.read_sql_query(
            "SELECT name AS table_name "
            "FROM sqlite_master "
            "WHERE type='table' "
            "ORDER BY name;",
            conn
        )
    finally:
        conn.close()

    # Выводим результат
    print("\n📋 Список таблиц в БД:\n")
    print(tables_df.to_string(index=False))

if __name__ == "__main__":
    main()
