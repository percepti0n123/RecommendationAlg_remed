import argparse
import logging
from tabulate import tabulate

from db.db import load_data



from dev.markdown_report import save_markdown_report
from recommendation_algo.services.recommendation_service import content_based_recommendations
from recommendation_algo.repository.task_repo import get_completed_task_ids

logging.basicConfig(filename="logs/recommendation.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description="Рекомендательная система для подготовки к ЕГЭ")
    parser.add_argument('--student_id', type=int, help="ID студента", required=False)
    parser.add_argument('--export_path', type=str, help="Путь для сохранения CSV", required=False)

    args = parser.parse_args()

    # Загружаем данные
    students, tasks, lessons, lesson_tasks, exam_results, exam_tasks, student_theme_progress = load_data()
    from db.db import create_data, insert_data
    create_data()
    insert_data()

    if any(df is None for df in [students, tasks, lessons, exam_results, exam_tasks, student_theme_progress]):
        print("❌ Ошибка при загрузке данных.")
        return

    # Получение ID студента
    student_id = args.student_id
    if not student_id:
        student_id = int(input("Введите ID студента: "))

    # Получение ID выполненных заданий (для совместимости с CB)
    completed_task_ids = get_completed_task_ids(student_id)

    # Запуск content-based рекомендаций
    recommendations = content_based_recommendations(student_id)
    print("\n📘 Content-Based рекомендации:")

    if recommendations.empty:
        print("⚠️ Нет рекомендаций для отображения.")
        return

    # Отображаем таблицу
    table = recommendations[['id', 'theme_name', 'explanation', 'source']].head(20)
    print(tabulate(table, headers="keys", tablefmt="fancy_grid"))



    # Сохраняем, если указан путь
    if args.export_path:
        try:
            recommendations.to_csv(args.export_path, index=False)
            logging.info(f"Рекомендации сохранены в {args.export_path}")
            print(f"\n📁 Рекомендации сохранены в файл: {args.export_path}")

            md_path = args.export_path.replace(".csv", ".md")
            save_markdown_report(recommendations, md_path, student_id)
        except Exception as e:
            logging.error(f"Ошибка при сохранении CSV: {e}")
            print(f"Ошибка при сохранении файла: {e}")

import matplotlib.pyplot as plt
from collections import Counter

def plot_explanation_distribution(recommendations):
    # Собираем все объяснения в один список
    explanation_flat = [e for expl in recommendations['explanation'] for e in expl]
    counts = Counter(explanation_flat)

    # Построение pie chart
    labels = counts.keys()
    sizes = counts.values()

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("🔍 Распределение оснований для рекомендаций")
    plt.axis("equal")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
