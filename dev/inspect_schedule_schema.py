# dev/inspect_schedule_schema.py
import sqlite3
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(Schedule)")
columns = cursor.fetchall()

print("📋 Поля таблицы Schedule:")
for column in columns:
    print(column)

conn.close()
