import sys
import pandas as pd

sys.path.append('./recommendation_algo')  # путь к папке проекта

from recommendation_algo.services.recommendation_service import content_based_recommendations
from db.db import load_data

# Загружаем данные
students, tasks, lessons, lesson_tasks, exam_results, exam_tasks, student_theme_progress = load_data()

# Протестируем трёх студентов
test_students = [201, 202, 203]

for student_id in test_students:
    print(f"\n🧪 ДИАГНОСТИКА: Студент ID {student_id}")

    # Получаем рекомендации
    recommendations = content_based_recommendations(student_id)

    if recommendations.empty:
        print("❌ Нет рекомендаций.")
        continue

    # Распечатаем до 10 строк
    display_df = recommendations[['id', 'theme_name', 'explanation']].head(10)
    pd.set_option('display.max_colwidth', None)
    print(display_df)
