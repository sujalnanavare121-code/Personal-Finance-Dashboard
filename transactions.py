from database import connect_db

def add_transaction(date, transaction_type, category, amount):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transactions (date, type, category, amount) VALUES (?, ?, ?, ?)",
        (date, transaction_type, category, amount)
    )

    conn.commit()
    conn.close()

def get_all_transactions():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transactions ORDER BY id")
    transactions = cursor.fetchall()

    conn.close()
    return transactions

def edit_transaction(transaction_id, date, transaction_type, category, amount):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        """UPDATE transactions
           SET date = ?, type = ?, category = ?, amount = ?
           WHERE id = ?""",
        (date, transaction_type, category, amount, transaction_id)
    )

    conn.commit()
    conn.close()

def delete_transaction(transaction_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    conn.commit()
    conn.close()