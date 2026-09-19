import json
import csv
import os
import shutil

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
    # Always create a fresh JSON file from database
    save_json()

    # Copy fresh JSON as backup
    shutil.copy(JSON_FILE, BACKUP_FILE)

    print("\nBackup created successfully!")
    print("File:", BACKUP_FILE)


def restore_data():
    if not os.path.exists(BACKUP_FILE):
        print("\nNo backup file found.")
        return False

    with open(BACKUP_FILE, "r") as file:
        data = json.load(file)

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")

    for transaction in data:
        cursor.execute(
            """
            INSERT INTO transactions
            (date, type, category, amount)
            VALUES (?, ?, ?, ?)
            """,
            (
                transaction["date"],
                transaction["type"],
                transaction["category"],
                transaction["amount"]
            )
        )

    conn.commit()
    conn.close()

    save_json()

    print("\nData restored successfully!")

    return True


def export_csv():
    transactions = get_transactions()

    if len(transactions) == 0:
        print("\nNo transactions to export.")
        return

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

    print("\nCSV exported successfully!")
    print("File:", CSV_FILE)