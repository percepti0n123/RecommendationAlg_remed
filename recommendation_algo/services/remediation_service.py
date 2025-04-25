# recommendation_algo/services/remediation_service.py

import pandas as pd
from recommendation_algo.repository import task_repo, progress_repo, student_repo

GRADE_THRESHOLD = 90  # ниже этого считается "неуспешно"


def generate_remediation(student_id: int, block_id: int) -> pd.DataFrame:
    """
    Формирует отработку для студента по заданному блоку (задание ЕГЭ).
    Возвращает DataFrame с задачами, которые нужно отработать.
    """
    # Шаг 1. Получаем задачи, которые решал студент в рамках блока
    attempted_tasks = task_repo.get_tasks_by_student_and_block(student_id, block_id)

    if attempted_tasks.empty:
        print(f"❗ Студент {student_id} не решал задач в блоке {block_id}")
        return pd.DataFrame()

    # Шаг 2. Выбираем неуспешные задачи
    failed_tasks = attempted_tasks[attempted_tasks["grade"] < GRADE_THRESHOLD]

    if failed_tasks.empty:
        print(f"✅ Все задачи решены успешно — отработка не требуется")
        return pd.DataFrame()

    # Шаг 3. Определяем темы, по которым были ошибки
    weak_theme_ids = failed_tasks["theme_id"].dropna().unique().tolist()

    # Шаг 4. Подбираем альтернативные задачи по этим темам
    similar_tasks = task_repo.get_tasks_by_themes(weak_theme_ids)

    # Шаг 5. Исключаем уже решённые
    completed_ids = attempted_tasks["id"].tolist()
    remediation_tasks = similar_tasks[~similar_tasks["id"].isin(completed_ids)]

    # Добавляем объяснение
    remediation_tasks = remediation_tasks.copy()
    remediation_tasks["explanation"] = "ошибка по теме в блоке"
    remediation_tasks["source"] = "remediation"

    return remediation_tasks[["id", "description", "theme_id", "theme_name", "complexity", "explanation", "source"]]
