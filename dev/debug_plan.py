# dev/debug_plan.py

from recommendation_algo.services.plan_service import generate_personal_plan
from tabulate import tabulate

print("🔍 DEBUG: Personal Plan Generation\n")

student_id = 204  # ID студента, для которого строим план

try:
    personal_plan_df = generate_personal_plan(student_id)

    if personal_plan_df.empty:
        print("⚠️ План пуст — возможно, нет данных по студенту или курсу.")
    else:
        print(tabulate(personal_plan_df, headers="keys", tablefmt="fancy_grid"))
except Exception as e:
    print(f"❌ Ошибка: {e}")
