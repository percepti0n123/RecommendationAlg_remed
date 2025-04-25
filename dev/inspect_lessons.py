# dev/inspect_lessons.py
import sqlite3
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT id, section_id FROM Lessons WHERE id = 1")
print(cursor.fetchall())
conn.close()
