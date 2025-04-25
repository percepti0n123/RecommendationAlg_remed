import sqlite3
from datetime import datetime
from db.db import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

student_id = 204
print(f"👤 Добавляем студента {student_id}")
cursor.execute("INSERT OR IGNORE INTO Students (id, name, phone_number, email) VALUES (?, ?, ?, ?)",
               (student_id, f"Student {student_id}", "+70000000000", f"student{student_id}@mail.ru"))

cursor.execute("INSERT OR IGNORE INTO Schedule (student_id) VALUES (?)", (student_id,))
cursor.execute("SELECT id FROM Schedule WHERE student_id = ?", (student_id,))
schedule_id = cursor.fetchone()[0]
print(f"📅 Schedule ID: {schedule_id}")

# Настройка блоков (section_id = 1..10)
for block_id in range(1, 11):
    cursor.execute("SELECT id FROM Lessons WHERE section_id = ?", (block_id,))
    lessons = cursor.fetchall()
    if not lessons:
        print(f"⚠️ Нет уроков в блоке {block_id}, пропускаем")
        continue

    for lesson_id in lessons:
        lesson_id = lesson_id[0]
        cursor.execute("INSERT OR IGNORE INTO Schedule_lessons (schedule_id, lesson_id, deadline, percentage) VALUES (?, ?, ?, ?)",
                       (schedule_id, lesson_id, '2025-04-25', 100.0))

        # Получаем задачи урока
        cursor.execute("SELECT task_id FROM Lesson_tasks WHERE lesson_id = ?", (lesson_id,))
        tasks = cursor.fetchall()

        for task in tasks:
            task_id = task[0]
            # Успешные (1–5) — grade=90, Ошибки (6–9) — grade=50, Не решено (10) — пропускаем
            if block_id <= 5:
                grade = 90
            elif 6 <= block_id <= 9:
                grade = 50
            else:
                continue  # block_id == 10 — студент не решал

            cursor.execute("INSERT OR REPLACE INTO Lesson_tasks (lesson_id, task_id, grade) VALUES (?, ?, ?)",
                           (lesson_id, task_id, grade))

print("✅ Студент 204 настроен. Все данные добавлены.")
conn.commit()
conn.close()
