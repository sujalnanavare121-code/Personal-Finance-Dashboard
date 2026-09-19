from database import connect_db

def calculate_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'income'")
    income = cursor.fetchone()[0] or 0

    cursor.execute("SELECT SUM(amount) FROM transactions WHERE type = 'expense'")
    expense = cursor.fetchone()[0] or 0

    balance = income - expense

    conn.close()

    return income, expense, balance

def monthly_summary(month):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type = 'income' AND substr(date, 4, 7) = ?",
        (month,)
    )
    income = cursor.fetchone()[0] or 0

    cursor.execute(
        "SELECT SUM(amount) FROM transactions WHERE type = 'expense' AND substr(date, 4, 7) = ?",
        (month,)
    )
    expense = cursor.fetchone()[0] or 0

    balance = income - expense

    conn.close()

    return income, expense, balance

def highest_expense_category():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, SUM(amount)
        FROM transactions
        WHERE type = 'expense'
        GROUP BY category
        ORDER BY SUM(amount) DESC
        LIMIT 1
    """)

    result = cursor.fetchone()

    conn.close()

    return result

def search_transactions(category):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM transactions WHERE category LIKE ?",
        (f"%{category}%",)
    )

    results = cursor.fetchall()

    conn.close()

    return results