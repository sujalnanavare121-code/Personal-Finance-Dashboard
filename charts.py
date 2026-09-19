import os
import matplotlib.pyplot as plt
from database import connect_db

CHART_FOLDER = "charts"

def create_expense_chart():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
    """)

    data = cursor.fetchall()
    conn.close()

    if not data:
        print("No expense data available!")
        return

    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    os.makedirs(CHART_FOLDER, exist_ok=True)

    plt.figure(figsize=(8, 5))
    plt.pie(amounts, labels=categories, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.tight_layout()

    chart_path = os.path.join(CHART_FOLDER, "expense_chart.png")
    plt.savefig(chart_path)
    plt.close()

    print(f"Chart created successfully! File: {chart_path}")