import sqlite3
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("📋 Schedule:")
for row in cursor.execute("SELECT * FROM Schedule"):
    print(row)

print("\n📋 Schedule_lessons:")
for row in cursor.execute("SELECT * FROM Schedule_lessons"):
    print(row)

conn.close()
