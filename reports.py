from database import connect_db


def calculate_summary():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, category, amount
        FROM transactions
    """)

    transactions = cursor.fetchall()

    total_income = 0
    total_expense = 0
    category_expenses = {}

    for transaction in transactions:
        transaction_type = transaction[0]
        category = transaction[1]
        amount = transaction[2]

        if transaction_type == "income":
            total_income += amount

        elif transaction_type == "expense":
            total_expense += amount

            category_expenses[category] = (
                category_expenses.get(category, 0) + amount
            )

    balance = total_income - total_expense

    conn.close()

    return total_income, total_expense, balance, category_expenses


def monthly_summary(month):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, type, category, amount
        FROM transactions
    """)

    transactions = cursor.fetchall()

    total_income = 0
    total_expense = 0
    category_expenses = {}

    for transaction in transactions:
        date = transaction[0]
        transaction_type = transaction[1]
        category = transaction[2]
        amount = transaction[3]

        if date[3:10] == month:
            if transaction_type == "income":
                total_income += amount

            elif transaction_type == "expense":
                total_expense += amount

                category_expenses[category] = (
                    category_expenses.get(category, 0) + amount
                )

    balance = total_income - total_expense

    conn.close()

    return (
        total_income,
        total_expense,
        balance,
        category_expenses
    )


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