import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger("db_helper")
@contextmanager
def get_db_connector(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager")

    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()

    cursor.close()
    connection.close()


def fetch_expenses_for_date(date):
    logger.info(f"fetch_expenses_for_date called with {date}")
    with get_db_connector() as cursor:
        cursor.execute("select * from expenses where expense_date = %s", (date,))
        expenses = cursor.fetchall()
        return expenses


def delete_expense_for_date(date):
    logger.info(f"delete_expense_for_date called with {date}")
    with get_db_connector(commit=True) as cursor:
        cursor.execute("delete from expenses where expense_date = %s", (date,))


def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount},category: {category},notes: {notes}")
    with get_db_connector(commit=True) as cursor:
        cursor.execute("insert into expenses (expense_date, amount, category, notes) values (%s,%s,%s, %s)",
                       (expense_date, amount, category, notes))


def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary called with start date: {start_date} and end date: {end_date}")
    with get_db_connector() as cursor:
        cursor.execute(
            "select category, sum(amount) as Total from expenses where expense_date between %s and %s group by category",
            (start_date, end_date,))
        data = cursor.fetchall()
        return data

def fetch_expense_by_month():
    with get_db_connector() as cursor:
        cursor.execute("""
                    SELECT MONTH(expense_date) AS Month_no, 
                    DATE_FORMAT(expense_date, '%M %Y') AS Month,
                           SUM(amount) AS Total_amount
                    FROM expenses
                    GROUP BY DATE_FORMAT(expense_date, '%M %Y'),
                             YEAR(expense_date),
                             MONTH(expense_date)
                    ORDER BY YEAR(expense_date), MONTH(expense_date)
                """)
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-09-23")
    # expenses = fetch_expense_summary("2024-08-01", "2024-08-08")
    # delete_expense_for_date("2024-09-23")
    # insert_expense("2024-09-23", 850, "Entertainment", "Dhurandhar movie tickets")
    expenses = fetch_expense_by_month()
    for expense in expenses:
        print(expense)
