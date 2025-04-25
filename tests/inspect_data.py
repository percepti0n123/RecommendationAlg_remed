import sqlite3
import pandas as pd

# Подключаемся к базе
conn = sqlite3.connect('../your_database.db')

# Запрос прогресса
progress_df = pd.read_sql_query("SELECT * FROM StudentThemeProgress WHERE student_id IN (201,202,203);", conn)
print("Прогресс по темам:\n", progress_df)

# Запрос анкет
forms_df = pd.read_sql_query("SELECT * FROM Forms WHERE student_id IN (201,202,203);", conn)
print("Анкеты:\n", forms_df)

conn.close()
