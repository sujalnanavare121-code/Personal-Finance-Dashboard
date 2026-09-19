from datetime import datetime

from database import connect_db, create_database

from transactions import (
    add_transaction as db_add_transaction,
    get_all_transactions as db_get_all_transactions,
    edit_transaction as db_edit_transaction,
    delete_transaction as db_delete_transaction
)

from reports import (
    calculate_summary as db_calculate_summary,
    monthly_summary as db_monthly_summary,
    highest_expense_category as db_highest_expense_category,
    search_transactions as db_search_transactions
)

from backup import (
    save_json,
    backup_data as db_backup_data,
    restore_data as db_restore_data,
    export_csv as db_export_csv
)

from charts import create_expense_chart as db_create_expense_chart

DB_FILE = "finance.db"
JSON_FILE = "transactions.json"
CSV_FILE = "transactions.csv"
BACKUP_FILE = "backup.json"
CHART_FOLDER = "charts"


# ==================== VALIDATION ====================

def get_date(message="Enter date (DD-MM-YYYY): "):
    while True:
        date = input(message).strip()

        try:
            datetime.strptime(date, "%d-%m-%Y")
            return date
        except ValueError:
            print("Invalid date! Please use DD-MM-YYYY.")

def get_transaction_type(message="Enter transaction type (income/expense): "):
    while True:
        transaction_type = input(message).lower().strip()

        if transaction_type in ["income", "expense"]:
            return transaction_type

        print("Invalid transaction type!")

def get_amount(message="Enter amount: "):
    while True:
        try:
            amount = float(input(message))

            if amount > 0:
                return amount

            print("Amount must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")

def pause():
    input("\nPress Enter to continue...")

# ==================== TRANSACTION FUNCTIONS ====================

def add_transaction():
    print("\n----- Add Transaction -----")

    date = get_date()
    transaction_type = get_transaction_type()
    category = input("Enter category: ").strip()

    while category == "":
        print("Category cannot be empty.")
        category = input("Enter category: ").strip()

    amount = get_amount()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions(date,type,category,amount)
        VALUES(?,?,?,?)
    """, (date, transaction_type, category, amount))

    conn.commit()
    conn.close()


    print("\nTransaction added successfully!")
    pause()

def get_all_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id,date,type,category,amount
        FROM transactions
        ORDER BY id
    """)

    transactions = cursor.fetchall()
    conn.close()

    return transactions

def view_transactions():
    transactions = get_all_transactions()

    print("\n----- Transactions -----")

    if len(transactions) == 0:
        print("No transactions found.")
        pause()
        return

    for transaction in transactions:
        print(
            transaction[0], ".",
            transaction[1], "-",
            transaction[2], "-",
            transaction[3], "- ₹",
            transaction[4]
        )

    pause()

def edit_transaction():
    transactions = get_all_transactions()

    if len(transactions) == 0:
        print("\nNo transactions available to edit.")
        pause()
        return

    view_transactions()

    while True:
        try:
            transaction_id = int(
                input("\nEnter transaction ID to edit: ")
            )

            if any(t[0] == transaction_id for t in transactions):
                break

            print("Invalid transaction ID.")

        except ValueError:
            print("Please enter a valid number.")

    print("\nEnter new transaction details.")

    new_date = get_date()
    new_type = get_transaction_type()
    new_category = input("Enter new category: ").strip()

    while new_category == "":
        print("Category cannot be empty.")
        new_category = input("Enter new category: ").strip()

    new_amount = get_amount()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE transactions
        SET date=?,type=?,category=?,amount=?
        WHERE id=?
    """, (
        new_date,
        new_type,
        new_category,
        new_amount,
        transaction_id
    ))

    conn.commit()
    conn.close()


    print("\nTransaction updated successfully!")
    pause()

def delete_transaction():
    transactions = get_all_transactions()

    if len(transactions) == 0:
        print("\nNo transactions available to delete.")
        pause()
        return

    view_transactions()

    while True:
        try:
            transaction_id = int(
                input("\nEnter transaction ID to delete: ")
            )

            if any(t[0] == transaction_id for t in transactions):
                break

            print("Invalid transaction ID.")

        except ValueError:
            print("Please enter a valid number.")

    confirm = input(
        "Are you sure you want to delete it? (yes/no): "
    ).lower().strip()

    if confirm != "yes":
        print("Delete cancelled.")
        pause()
        return

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id=?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()


    print("\nTransaction deleted successfully!")
    pause()

# ==================== SUMMARY & ANALYTICS ====================

def calculate_summary(transactions):
    total_income = 0
    total_expense = 0
    category_expenses = {}

    for transaction in transactions:
        transaction_type = transaction[2]
        category = transaction[3]
        amount = transaction[4]

        if transaction_type == "income":
            total_income += amount

        elif transaction_type == "expense":
            total_expense += amount

            category_expenses[category] = (
                category_expenses.get(category, 0) + amount
            )

    balance = total_income - total_expense

    return total_income, total_expense, balance, category_expenses

def show_summary():
    transactions = get_all_transactions()

    if len(transactions) == 0:
        print("\nNo transactions available.")
        pause()
        return

    total_income, total_expense, balance, category_expenses = (
        calculate_summary(transactions)
    )

    print("\n================================")
    print("       FINANCE SUMMARY")
    print("================================")

    print("Total Income  :", total_income)
    print("Total Expense :", total_expense)
    print("Balance       :", balance)

    print("\n----- Category-wise Expenses -----")

    if len(category_expenses) == 0:
        print("No expenses found.")

    else:
        for category, amount in category_expenses.items():
            print(category, ":", amount)

    pause()

def monthly_summary():
    transactions = get_all_transactions()

    if len(transactions) == 0:
        print("\nNo transactions available.")
        pause()
        return

    while True:
        month = input("\nEnter month (MM-YYYY): ").strip()

        try:
            datetime.strptime(month, "%m-%Y")
            break

        except ValueError:
            print("Invalid month! Please use MM-YYYY.")

    monthly_transactions = []

    for transaction in transactions:
        try:
            transaction_month = datetime.strptime(
                transaction[1],
                "%d-%m-%Y"
            ).strftime("%m-%Y")

            if transaction_month == month:
                monthly_transactions.append(transaction)

        except ValueError:
            continue

    if len(monthly_transactions) == 0:
        print("\nNo transactions found for", month)
        pause()
        return

    total_income, total_expense, balance, category_expenses = (
        calculate_summary(monthly_transactions)
    )

    print("\n================================")
    print("     MONTHLY FINANCE SUMMARY")
    print("================================")

    print("Month         :", month)
    print("Total Income  :", total_income)
    print("Total Expense :", total_expense)
    print("Balance       :", balance)

    print("\n----- Category-wise Expenses -----")

    for category, amount in category_expenses.items():
        print(category, ":", amount)

    pause()

def highest_expense_category():
    transactions = get_all_transactions()

    _, _, _, category_expenses = calculate_summary(transactions)

    if len(category_expenses) == 0:
        print("\nNo expenses found.")
        pause()
        return

    category = max(
        category_expenses,
        key=category_expenses.get
    )

    amount = category_expenses[category]

    print("\n----- Highest Expense Category -----")
    print("Category:", category)
    print("Amount  : ₹", amount)

    pause()

# ==================== SEARCH ====================

def search_transactions():
    transactions = get_all_transactions()

    if len(transactions) == 0:
        print("\nNo transactions available.")
        pause()
        return

    print("\n----- Search Transactions -----")
    print("1. Search by category")
    print("2. Search by type")
    print("3. Search by date")
    print("4. Search by amount")
    print("5. Back")

    choice = input("\nEnter choice: ").strip()

    results = []

    if choice == "1":
        keyword = input("Enter category: ").lower().strip()

        for transaction in transactions:
            if keyword in transaction[3].lower():
                results.append(transaction)

    elif choice == "2":
        transaction_type = get_transaction_type()

        for transaction in transactions:
            if transaction[2] == transaction_type:
                results.append(transaction)

    elif choice == "3":
        date = get_date()

        for transaction in transactions:
            if transaction[1] == date:
                results.append(transaction)

    elif choice == "4":
        amount = get_amount()

        for transaction in transactions:
            if transaction[4] == amount:
                results.append(transaction)

    elif choice == "5":
        return

    else:
        print("Invalid choice.")
        pause()
        return

    print("\n----- Search Results -----")

    if len(results) == 0:
        print("No matching transactions found.")

    else:
        for transaction in results:
            print(
                transaction[0], ".",
                transaction[1], "-",
                transaction[2], "-",
                transaction[3], "- ₹",
                transaction[4]
            )

    pause()

# ==================== BUDGET ====================

def set_budget():
    budget = get_amount("\nEnter monthly budget: ")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO settings(key,value)
        VALUES('monthly_budget',?)
    """, (budget,))

    conn.commit()
    conn.close()

    print("\nMonthly budget set to ₹", budget)
    pause()

def get_budget():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT value
        FROM settings
        WHERE key='monthly_budget'
    """)

    result = cursor.fetchone()
    conn.close()

    if result is None:
        return 0

    return result[0]

def budget_status():
    budget = get_budget()

    if budget == 0:
        print("\nNo monthly budget set.")
        pause()
        return

    month = datetime.now().strftime("%m-%Y")

    transactions = get_all_transactions()

    monthly_expense = 0

    for transaction in transactions:
        try:
            transaction_month = datetime.strptime(
                transaction[1],
                "%d-%m-%Y"
            ).strftime("%m-%Y")

            if (
                transaction_month == month
                and transaction[2] == "expense"
            ):
                monthly_expense += transaction[4]

        except ValueError:
            continue

    remaining = budget - monthly_expense

    print("\n================================")
    print("          BUDGET STATUS")
    print("================================")

    print("Month          :", month)
    print("Budget         :", budget)
    print("Current Expense:", monthly_expense)
    print("Remaining      :", remaining)

    if remaining < 0:
        print("\nWARNING: Budget exceeded!")

    elif remaining == 0:
        print("\nBudget completely used.")

    else:
        print("\nBudget remaining:", remaining)

    pause()

# ==================== JSON BACKUP ====================

def backup_data():
    db_backup_data()
    pause()


def restore_data():
    result = db_restore_data()
    pause()
    return result
# ==================== CSV EXPORT ====================

def export_csv():
    db_export_csv()

# ==================== CHARTS ====================

def create_expense_chart():
    db_create_expense_chart()

# ==================== DASHBOARD ====================

def dashboard():
    transactions = get_all_transactions()

    total_income, total_expense, balance, category_expenses = (
        calculate_summary(transactions)
    )

    budget = get_budget()

    print("\n========================================")
    print("       PERSONAL FINANCE DASHBOARD")
    print("========================================")

    print("\nIncome  :", total_income)
    print("Expense :", total_expense)
    print("Balance :", balance)

    if budget > 0:
        print("Budget  :", budget)
        print("Used   :", total_expense)
        print("Left   :", budget - total_expense)

    print("\n----- TOP EXPENSE CATEGORIES -----")

    if len(category_expenses) == 0:
        print("No expenses found.")

    else:
        sorted_categories = sorted(
            category_expenses.items(),
            key=lambda x: x[1],
            reverse=True
        )

        for category, amount in sorted_categories[:5]:
            print(category, ":", amount)

    pause()

# ==================== MAIN MENU ====================

def main():
    create_database()

    while True:
        print("\n========================================")
        print("       PERSONAL FINANCE DASHBOARD")
        print("========================================")

        print("\n1. Add Transaction")
        print("2. View Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Finance Summary")
        print("6. Monthly Summary")
        print("7. Search Transactions")
        print("8. Set Monthly Budget")
        print("9. Budget Status")
        print("10. Highest Expense Category")
        print("11. Export to CSV")
        print("12. Create Expense Chart")
        print("13. Dashboard")
        print("14. Backup Data")
        print("15. Restore Data")
        print("16. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_transaction()

        elif choice == "2":
            view_transactions()

        elif choice == "3":
            edit_transaction()

        elif choice == "4":
            delete_transaction()

        elif choice == "5":
            show_summary()

        elif choice == "6":
            monthly_summary()

        elif choice == "7":
            search_transactions()

        elif choice == "8":
            set_budget()

        elif choice == "9":
            budget_status()

        elif choice == "10":
            highest_expense_category()

        elif choice == "11":
            export_csv()

        elif choice == "12":
            create_expense_chart()

        elif choice == "13":
            dashboard()

        elif choice == "14":
            backup_data()

        elif choice == "15":
            restore_data()

        elif choice == "16":
            print("\nThank you for using Personal Finance Dashboard!")
            break

        else:
            print("\nInvalid choice! Please enter 1 to 16.")
            pause()

if __name__ == "__main__":
    main()