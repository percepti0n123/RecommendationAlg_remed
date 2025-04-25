import pandas as pd
from recommendation_algo.repository import student_repo, task_repo, forms_repo, progress_repo

def content_based_recommendations(student_id):
    """
    Контентно-ориентированные рекомендации:
    - Учитывает предпочтения из анкеты
    - Темы с низким прогрессом
    - Исключает выполненные задания
    - Объясняет каждую рекомендацию
    """
    # Проверка, есть ли студент
    student_info = student_repo.get_student_by_id(student_id)
    if student_info.empty:
        return pd.DataFrame()

    # Получение данных
    preferences = forms_repo.get_student_preferences(student_id)
    completed_task_ids = task_repo.get_completed_task_ids(student_id)
    tasks_with_theme = task_repo.get_tasks_with_themes()
    student_progress = progress_repo.get_student_theme_progress(student_id)

    # Обработка предпочтений
    if isinstance(preferences, str):
        preferences = [p.strip() for p in preferences.split(',')]

    # Темы с низким прогрессом
    progress_threshold = 70.0
    low_progress_themes = student_progress[student_progress['progress'] < progress_threshold]['theme_id'].tolist()

    # Отладочный вывод
    print(f"\n📌 DEBUG для студента {student_id}")
    print("🔹 Предпочтения:", preferences)
    print("🔹 Темы с низким прогрессом:", low_progress_themes)

    # Исключаем выполненные задания
    candidate_tasks = tasks_with_theme[~tasks_with_theme['id'].isin(completed_task_ids)]
    print("🔹 theme_id в кандидатах:", candidate_tasks['theme_id'].unique().tolist())

    # Фильтрация по интересам (анкета)
    if preferences:
        pref_filtered = candidate_tasks[
            candidate_tasks['theme_name'].str.contains('|'.join(preferences), case=False, na=False)
        ]
        print(f"✅ Найдено по интересам: {len(pref_filtered)} задач")
        candidate_tasks = pref_filtered

    # Фильтрация по темам с низким прогрессом
    recommended_tasks = candidate_tasks[candidate_tasks['theme_id'].isin(low_progress_themes)]
    print(f"✅ Найдено по слабым темам: {len(recommended_tasks)} задач")

    # Fallback: если ничего не найдено — показать все оставшиеся
    if recommended_tasks.empty:
        recommended_tasks = candidate_tasks
        print("⚠️ Нет задач по слабым темам — используем все оставшиеся")

    # Обоснование каждой задачи
    recommended_tasks = recommended_tasks.copy()
    recommended_tasks['explanation'] = recommended_tasks.apply(lambda task: [], axis=1)
    for i, task in recommended_tasks.iterrows():
        if any(pref.lower() in (task['theme_name'] or '').lower() for pref in preferences):
            recommended_tasks.at[i, 'explanation'].append("интерес ученика")
        if task['theme_id'] in low_progress_themes:
            recommended_tasks.at[i, 'explanation'].append("низкий прогресс по теме")
        if not recommended_tasks.at[i, 'explanation']:
            recommended_tasks.at[i, 'explanation'].append("не выполнено ранее")

    # Источник
    recommended_tasks['source'] = "content"

    return recommended_tasks[['id', 'section_id', 'description', 'complexity', 'theme_id', 'theme_name', 'explanation', 'source']]



from recommendation_algo.services.collaborative_service import get_collaborative_recommendations

def hybrid_recommendations(student_id, model_knn, exam_scores_matrix, tasks, exam_tasks, completed_task_ids):
    """
    Гибридные рекомендации: объединение content-based и collaborative подходов.
    """
    # Получаем обе части
    content_recs = content_based_recommendations(student_id)
    collab_recs = get_collaborative_recommendations(
        student_id, model_knn, exam_scores_matrix, tasks, exam_tasks, completed_task_ids
    )

    # Объединяем по id (уникальные рекомендации)
    all_recs = pd.concat([content_recs, collab_recs]).drop_duplicates(subset='id', keep='first')

    # Если задача была рекомендована в обеих — объединяем объяснение
    all_recs = all_recs.groupby('id', as_index=False).agg({
        'section_id': 'first',
        'description': 'first',
        'complexity': 'first',
        'theme_id': 'first',
        'theme_name': 'first',
        'explanation': lambda x: list(set(sum(x, []))),
        'source': lambda x: '+'.join(sorted(set(x)))
    })

    return all_recs