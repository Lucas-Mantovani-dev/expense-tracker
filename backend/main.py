from fastapi import FastAPI, HTTPException
from datetime import datetime
import models, services

app = FastAPI()

# CREATES A NEW EXPENSE
@app.post("/expenses")
def create_expense(new_expense: models.NewExpense):
    new_expense.amount = round(new_expense.amount, 2)
    return services.create_expense(request= new_expense)

# SHOWS EXPENSE LIST
@app.get("/expenses")
def get_expenses(
    category_id: int | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    search: str | None = None
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

    return services.get_expenses(query = query, param = tuple(parameters))

# RETRIEVE ONLY ONE EXPENSE
@app.get("/expenses/{expense_id}")
def get_expense(expense_id: int):
    return services.get_expense(expense_id)

# UPDATE PARTIAL CHANGES
@app.patch("/expenses/{expense_id}")
def patch_expense(expense_id: int, request: models.PatchExpense):
    query = "UPDATE expenses SET"
    parameters = []

    for attr, value in vars(request).items():
        if value:
            query += " ? = ?,"
            parameters.append(attr)
            parameters.append(value)

    if not parameters:
        HTTPException(
            status_code=400,
            detail="No changes attributed!"
        )

    else:
        query += " WHERE expense_id = ?"
        parameters.append(expense_id)
        return services.patch_expense(query, tuple(parameters), expense_id)

# DELETE EXPENSE
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int):
    return services.delete_expense(expense_id)

# GET CATEGORIES FOR CATEGORY DROPDOWN BUTTON
@app.get("/categories")
def get_categories():
    return services.get_categories()

# CREATE NEW CATEGORY
@app.post("/categories")
def post_categories(new_category: models.NewCategory):
    if services.check_category(new_category) == 1:
        HTTPException(
            status_code=409,
            detail="Category already exists!"
        )
    else:
        return services.create_category(new_category)

