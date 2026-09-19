# Personal Finance Dashboard

A Python-based personal finance management application that helps users track income and expenses, manage monthly budgets, analyze spending, and export financial data.

## Features

* Add income and expense transactions
* View all transactions
* Edit transactions
* Delete transactions
* Calculate total income, expenses, and balance
* Generate monthly financial summaries
* Search transactions
* Set monthly budgets
* Check budget status
* Find the highest expense category
* Export transactions to CSV
* Generate expense charts
* View a financial dashboard
* Backup data to JSON
* Restore data from JSON
* Store transaction data using SQLite
* Input validation for transactions

## Technologies Used

* Python
* SQLite
* JSON
* CSV
* Matplotlib
* Git
* GitHub

## Project Structure

```text
Personal Finance Tracker/
│
├── main.py
├── main_backup.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── finance.db
├── transactions.json
├── transactions.csv
├── backup.json
│
└── charts/
```

> Local financial data files are excluded from GitHub using `.gitignore`.

## Requirements

* Python 3.x
* Matplotlib

Install the required dependency using:

```bash
pip install -r requirements.txt
```

## How to Run

Clone the repository:

```bash
git clone https://github.com/sujalnanavare121-code/Personal-Finance-Dashboard.git
```

Go to the project folder:

```bash
cd Personal-Finance-Dashboard
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## Database

The application uses SQLite to store transaction data locally.

The database file is:

```text
finance.db
```

## Data Backup

The application supports:

* JSON backup
* JSON restore
* CSV export

These files are kept locally and are excluded from the GitHub repository.

## Dashboard

The dashboard provides a quick overview of:

* Total income
* Total expenses
* Current balance
* Expense categories
* Budget information

## Learning Objectives

This project was built to practice practical Python and software development concepts including:

* Functions
* Lists and dictionaries
* File handling
* JSON handling
* CSV handling
* SQLite database operations
* Data validation
* Exception handling
* Data visualization
* Git and GitHub
* Project structure

## Future Improvements

Possible future improvements include:

* Login and authentication
* Multiple user support
* Advanced financial analytics
* More interactive charts
* Web-based interface
* Machine learning based expense prediction
* Expense category prediction
* Monthly spending recommendations

## Author

**Sujal Nanavare**

GitHub:
https://github.com/sujalnanavare121-code
