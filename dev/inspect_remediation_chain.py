import sqlite3
from db.db import DB_PATH

student_id = 202
block_id = 16

print(f"🔍 Проверка связей для студента {student_id} и блока {block_id}")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1. Получаем Schedule
cursor.execute("SELECT id FROM Schedule WHERE student_id = ?", (student_id,))
schedule = cursor.fetchone()
print("📌 Schedule:", schedule)

if not schedule:
    print("❌ Нет записи в Schedule")
    exit()

schedule_id = schedule[0]

# 2. Получаем Schedule_lessons
cursor.execute("SELECT lesson_id FROM Schedule_lessons WHERE schedule_id = ?", (schedule_id,))
schedule_lessons = cursor.fetchall()
print("📌 Schedule_lessons (lesson_ids):", [r[0] for r in schedule_lessons])

if not schedule_lessons:
    print("❌ Нет записей в Schedule_lessons")
    exit()

# 3. Фильтруем по block_id (section_id в Lessons)
lesson_ids = [r[0] for r in schedule_lessons]
placeholders = ",".join("?" * len(lesson_ids))
query = f"""
    SELECT id FROM Lessons 
    WHERE id IN ({placeholders}) AND section_id = ?
"""
cursor.execute(query, (*lesson_ids, block_id))
lessons_in_block = cursor.fetchall()
print("📌 Lessons в блоке:", [r[0] for r in lessons_in_block])

if not lessons_in_block:
    print("❌ Нет уроков в нужном блоке")
    exit()

lesson_ids_in_block = [r[0] for r in lessons_in_block]

# 4. Смотрим Lesson_tasks
placeholders = ",".join("?" * len(lesson_ids_in_block))
query = f"""
    SELECT lesson_id, task_id, grade FROM Lesson_tasks
    WHERE lesson_id IN ({placeholders})
"""
cursor.execute(query, lesson_ids_in_block)
lesson_tasks = cursor.fetchall()
print("📌 Lesson_tasks (с оценками):")
for row in lesson_tasks:
    print("   📘", row)

if not lesson_tasks:
    print("❌ Нет задач в уроках блока")
else:
    print("✅ Цепочка данных установлена")

conn.close()
