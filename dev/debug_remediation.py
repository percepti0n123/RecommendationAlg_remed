# dev/debug_remediation.py

from recommendation_algo.services.remediation_service import generate_remediation
from tabulate import tabulate

print("🔍 DEBUG: Remediation Recommendations\n")

student_id = 204
blocks_to_check = list(range(1, 11))  # Блоки 1–10

for block_id in blocks_to_check:
    print(f"\n🧪 Студент {student_id} | Блок {block_id}")
    remediation_df = generate_remediation(student_id, block_id)

    if remediation_df.empty:
        print("✅ Нет заданий для отработки.")
    else:
        display = remediation_df[["id", "theme_name", "explanation"]].head(10)
        print(tabulate(display, headers="keys", tablefmt="fancy_grid"))

    print("─" * 60)
