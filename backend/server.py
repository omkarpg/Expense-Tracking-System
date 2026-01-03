from fastapi import FastAPI,HTTPException
from datetime import date
import db_helper
from typing import List
from pydantic import BaseModel

app = FastAPI()

class Expenses(BaseModel):
    amount:float
    category: str
    notes: str

class DateRange(BaseModel):
    start_date:date
    end_date: date

@app.get("/expenses/{expense_date}", response_model=List[Expenses])
def get_expenses(expense_date: date):
    data = db_helper.fetch_expenses_for_date(expense_date)
    return data

@app.get("/analytics_by_month/")
def get_analytics_by_month():
    data = db_helper.fetch_expense_by_month()
    return data

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date:date, expenses:List[Expenses]):
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expense(expense_date,expense.amount,expense.category,expense.notes)

    return "Message: Expense updated successfully"

@app.post("/analytics/")
def get_analytics(date_range: DateRange):
    data = db_helper.fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code = 500, detail = f"Failed to retrieve expense summary from the database")
    total = 0
    for row in data:
        total += row['Total']

    breakdown = {}

    for row in data:
        percentage = (row['Total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            'total': row["Total"],
            'percentage': percentage
        }
    return breakdown
