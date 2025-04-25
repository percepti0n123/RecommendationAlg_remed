from db.db import load_data
from recommendation_algo.repository.task_repo import get_completed_task_ids
from recommendation_algo.services.collaborative_service import build_collaborative_model
from recommendation_algo.services.recommendation_service import hybrid_recommendations

STUDENT_IDS = [201, 202, 203]

students, tasks, lessons, lesson_tasks, exam_results, exam_tasks, student_theme_progress = load_data()
model_knn, exam_scores_matrix = build_collaborative_model(exam_results)

print("🔍 DEBUG: Hybrid Recommendations\n")

for sid in STUDENT_IDS:
    print(f"🧪 Студент {sid}")
    completed = get_completed_task_ids(sid)
    recommendations = hybrid_recommendations(
        sid, model_knn, exam_scores_matrix, tasks, exam_tasks, completed
    )

    if recommendations.empty:
        print("⚠️ Нет рекомендаций.")
    else:
        print(recommendations[['id', 'theme_name', 'explanation', 'source']].head(10))
    print("─" * 60)
