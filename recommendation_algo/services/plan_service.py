# services/plan_service.py
import pandas as pd
from recommendation_algo.repository import section_repo, theme_repo
from recommendation_algo.repository.forms_repo import get_student_form
from recommendation_algo.repository.student_repo import get_student_by_id


def generate_personal_plan(student_id: int) -> pd.DataFrame:
    """Сгенерировать индивидуальный план подготовки для ученика."""
    student = get_student_by_id(student_id)
    if student is None:
        raise ValueError(f"Студент с ID {student_id} не найден.")

    form = get_student_form(student_id)
    if form is None:
        raise ValueError(f"Анкета для студента {student_id} не найдена.")

    course_id = student["course_id"]
    preferences = eval(form["preferences"])

    # Получаем универсальный план и прогресс ученика
    universal_plan = theme_repo.get_universal_plan(course_id)
    progress = theme_repo.get_student_theme_progress(student_id)
    sections = section_repo.get_sections()

    # 1. Секции с низким прогрессом
    low_progress_sections = (
        progress[progress["progress"].fillna(0) < 70]["section_id"]
        .dropna()
        .unique()
        .tolist()
    )

    # 2. Приоритетная сортировка
    priority_list = []

    # Сначала по интересам ученика
    for section_id in universal_plan["section_id"]:
        section_name = sections[sections["id"] == section_id]["description"].values[0]
        if any(pref in section_name for pref in preferences):
            priority_list.append((section_id, "preference"))

    # Потом по слабым местам
    for section_id in universal_plan["section_id"]:
        if section_id in low_progress_sections and (section_id, "preference") not in priority_list:
            priority_list.append((section_id, "low_progress"))

    # Потом оставшиеся
    for section_id in universal_plan["section_id"]:
        if (section_id, "preference") not in priority_list and (section_id, "low_progress") not in priority_list:
            priority_list.append((section_id, "standard"))

    # Формируем финальный DataFrame
    plan = []
    for order, (section_id, reason) in enumerate(priority_list, start=1):
        section_name = sections[sections["id"] == section_id]["description"].values[0]
        plan.append({
            "order": order,
            "section_id": section_id,
            "section_name": section_name,
            "reason": reason
        })

    return pd.DataFrame(plan)
