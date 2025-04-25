# dev/inspect_schema.py
import sqlite3
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Получаем схему таблицы Schedule_lessons
cursor.execute("PRAGMA table_info(Schedule_lessons);")
columns = cursor.fetchall()

print("📋 Поля таблицы Schedule_lessons:")
for col in columns:
    print(col)

conn.close()
