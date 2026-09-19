import json
import csv
from database import connect_db

JSON_FILE = "transactions.json"
BACKUP_FILE = "backup.json"
CSV_FILE = "transactions.csv"

def get_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY id")
    transactions = cursor.fetchall()

    conn.close()
    return transactions

def save_json():
    transactions = get_transactions()

    data = []

    for transaction in transactions:
        data.append({
            "id": transaction[0],
            "date": transaction[1],
            "type": transaction[2],
            "category": transaction[3],
            "amount": transaction[4]
        })

    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def backup_data():
    transactions = get_transactions()

    data = []

    for transaction in transactions:
        data.append({
            "id": transaction[0],
            "date": transaction[1],
            "type": transaction[2],
            "category": transaction[3],
            "amount": transaction[4]
        })

    with open(BACKUP_FILE, "w") as file:
        json.dump(data, file, indent=4)

def restore_data():
    try:
        with open(BACKUP_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return False

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")

    for transaction in data:
        cursor.execute(
            """INSERT INTO transactions
               (date, type, category, amount)
               VALUES (?, ?, ?, ?)""",
            (
                transaction["date"],
                transaction["type"],
                transaction["category"],
                transaction["amount"]
            )
        )

    conn.commit()
    conn.close()

    return True

def export_csv():
    transactions = get_transactions()

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Date",
            "Type",
            "Category",
            "Amount"
        ])

        writer.writerows(transactions)