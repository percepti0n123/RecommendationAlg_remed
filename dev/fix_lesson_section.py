# dev/fix_lesson_section.py
import sqlite3
from db.db import DB_PATH

lesson_id = 16
correct_section_id = 14  # правильный номер блока/задания

print(f"🔧 Подключаемся к БД: {DB_PATH}")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT section_id FROM Lessons WHERE id = ?", (lesson_id,))
current_section = cursor.fetchone()

if current_section:
    print(f"📘 Lesson найден: (id={lesson_id}, section_id={current_section[0]})")
    cursor.execute("UPDATE Lessons SET section_id = ? WHERE id = ?", (correct_section_id, lesson_id))
    print(f"✅ Установлен section_id = {correct_section_id} для lesson_id = {lesson_id}")
else:
    print(f"❌ Урок с ID={lesson_id} не найден")

conn.commit()
conn.close()
