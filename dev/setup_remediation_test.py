# dev/setup_remediation_test.py
import sqlite3
from db.db import DB_PATH

print("🔧 Подключаемся к БД:", DB_PATH)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Получаем schedule_id для студента 202 или создаем, если его нет
cursor.execute("SELECT id FROM Schedule WHERE student_id = ?", (202,))
schedule = cursor.fetchone()
if schedule:
    schedule_id = schedule[0]
    print(f"📌 Schedule уже существует для студента 202 (ID={schedule_id})")
else:
    cursor.execute("INSERT INTO Schedule (student_id) VALUES (?)", (202,))
    schedule_id = cursor.lastrowid
    print(f"✅ Добавили Schedule для студента 202 — ID={schedule_id}")

# Добавляем урок 16 в Schedule_lessons, если его там нет
cursor.execute("""
    SELECT 1 FROM Schedule_lessons WHERE schedule_id = ? AND lesson_id = ?
""", (schedule_id, 16))
exists = cursor.fetchone()
if not exists:
    cursor.execute("""
        INSERT INTO Schedule_lessons (schedule_id, lesson_id, deadline, percentage)
        VALUES (?, ?, '2025-04-01', 60)
    """, (schedule_id, 16))
    print("✅ Добавили Lesson 16 студенту 202")

# Привязываем задачу 1 к уроку 16 (если еще не привязана)
cursor.execute("""
    SELECT 1 FROM Lesson_tasks WHERE lesson_id = ? AND task_id = ?
""", (16, 1))
exists = cursor.fetchone()
if not exists:
    cursor.execute("""
        INSERT INTO Lesson_tasks (lesson_id, task_id, grade)
        VALUES (?, ?, 60)
    """, (16, 1))
    print("✅ Установили grade=60 для student_id=202, lesson_id=16, task_id=1")
else:
    print("📌 Задача уже связана с уроком 16 — обновим grade")
    cursor.execute("""
        UPDATE Lesson_tasks SET grade = 60 WHERE lesson_id = ? AND task_id = ?
    """, (16, 1))


# === ДОБАВЛЯЕМ ПРОВАЛЬНУЮ ЗАДАЧУ ДЛЯ СТУДЕНТА 203 В БЛОКЕ 14 ===
print("\n🔧 Настраиваем данные для студента 203 и блока 14")

# Получаем schedule_id
cursor.execute("SELECT id FROM Schedule WHERE student_id = ?", (203,))
schedule = cursor.fetchone()
if schedule:
    schedule_id_203 = schedule[0]
    print(f"📌 Schedule уже существует для студента 203 (ID={schedule_id_203})")
else:
    cursor.execute("INSERT INTO Schedule (student_id) VALUES (?)", (203,))
    schedule_id_203 = cursor.lastrowid
    print(f"✅ Добавили Schedule для студента 203 — ID={schedule_id_203}")

# Получаем lesson_id из блока 14
cursor.execute("SELECT id FROM Lessons WHERE section_id = 14")
lesson_row = cursor.fetchone()
if lesson_row:
    lesson_id_203 = lesson_row[0]
    print(f"✅ Нашли lesson_id={lesson_id_203} из блока 14")
else:
    print("❌ Урока из блока 14 не найдено")
    conn.close()
    exit()

# Привязываем к расписанию
cursor.execute("""
    SELECT 1 FROM Schedule_lessons WHERE schedule_id = ? AND lesson_id = ?
""", (schedule_id_203, lesson_id_203))
exists = cursor.fetchone()
if not exists:
    cursor.execute("""
        INSERT INTO Schedule_lessons (schedule_id, lesson_id, deadline, percentage)
        VALUES (?, ?, '2025-04-10', 60)
    """, (schedule_id_203, lesson_id_203))
    print(f"✅ Добавили Lesson {lesson_id_203} студенту 203")
else:
    print(f"📌 Связь уже есть: schedule_id={schedule_id_203}, lesson_id={lesson_id_203}")

# Устанавливаем grade=60 для задачи 1
cursor.execute("""
    SELECT 1 FROM Lesson_tasks WHERE lesson_id = ? AND task_id = ?
""", (lesson_id_203, 1))
exists = cursor.fetchone()
if not exists:
    cursor.execute("""
        INSERT INTO Lesson_tasks (lesson_id, task_id, grade)
        VALUES (?, ?, 60)
    """, (lesson_id_203, 1))
    print(f"✅ Установили grade=60 для student_id=203, lesson_id={lesson_id_203}, task_id=1")
else:
    print(f"📌 Задача уже есть в уроке {lesson_id_203} — обновляем grade")
    cursor.execute("""
        UPDATE Lesson_tasks SET grade = 60 WHERE lesson_id = ? AND task_id = ?
    """, (lesson_id_203, 1))

conn.commit()
conn.close()
print("✅ Готово")
