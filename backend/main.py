from fastapi import FastAPI
from datetime import datetime
import models, services

app = FastAPI()

# CREATES A NEW EXPENSE
@app.post("/expenses")
def create_expense(new_expense: models.NewExpense):
    new_expense.amount = round(new_expense.amount, 2)
    expense_created = services.create_expense(request= new_expense)
    return expense_created

# SHOWS EXPENSE LIST
@app.get("/expenses")
def get_expenses(
    category_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    search: str | None = None,
):
    query = "SELECT * FROM expenses WHERE 1=1"
    parameters = []

    if category_id:
        query += " AND category_id = ?"
        parameters.append(category_id)

    if start_date:
        query += " AND date_time >= ?"
        parameters.append(start_date)
        if not end_date:
            now = datetime.now()
            formatted_str = now.strftime("%Y-%m-%d %H:%M:%S")
            query += " AND date_time < ?"
            parameters.append(formatted_str)

    if end_date:
        query += " AND date_time < ?"
        parameters.append(end_date)

    if search:
        query += " AND description LIKE ?"
        parameters.append(f"%{search}%")

    query += " SORT BY date_time DESC"

    response = services.get_expenses(query = query, param = tuple(parameters))