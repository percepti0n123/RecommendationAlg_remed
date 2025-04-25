import pandas as pd
from sklearn.neighbors import NearestNeighbors


def build_collaborative_model(exam_results):
    """
    Строит модель KNN на основе результатов экзаменов.
    """
    try:
        exam_scores_matrix = pd.pivot_table(
            exam_results,
            index='student_id',
            columns='exam_id',
            values='grade'
        ).fillna(0)

        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(exam_scores_matrix.values)

        return model_knn, exam_scores_matrix
    except Exception as e:
        print(f"Ошибка при построении модели CF: {e}")
        return None, None


def get_collaborative_recommendations(
    student_id,
    model_knn,
    exam_scores_matrix,
    tasks,
    exam_tasks,
    completed_task_ids
):
    """
    Выдаёт рекомендации задач на основе схожести результатов экзаменов с другими студентами.
    Исключает уже выполненные задания, добавляет объяснение и источник.
    """
    try:
        student_index = exam_scores_matrix.index.get_loc(student_id)
        distances, indices = model_knn.kneighbors(
            [exam_scores_matrix.iloc[student_index]],
            n_neighbors=min(3, len(exam_scores_matrix)-1)
        )
        similar_indices = indices.flatten()[1:]

        # Найдём задачи, которые решали похожие студенты
        recommended_task_ids = set()
        for idx in similar_indices:
            similar_student_id = exam_scores_matrix.index[idx]
            exams = exam_scores_matrix.loc[similar_student_id]
            for exam_id in exams[exams > 0].index:
                task_ids = exam_tasks[exam_tasks['exam_id'] == exam_id]['task_id']
                recommended_task_ids.update(task_ids)

        # Исключим выполненные
        recommended_task_ids -= set(completed_task_ids)

        # Выборка задач
        rec_tasks = tasks[tasks['id'].isin(recommended_task_ids)].copy()
        rec_tasks['explanation'] = [["похожий студент"] for _ in range(len(rec_tasks))]
        rec_tasks['source'] = "collaborative"

        return rec_tasks[['id', 'section_id', 'description', 'complexity', 'theme_id', 'theme_name', 'explanation', 'source']]

    except Exception as e:
        print(f"Ошибка в CF: {e}")
        return pd.DataFrame()
