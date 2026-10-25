import database
from datetime import datetime

def get_category(category_id: int):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(
        """SELECT * FROM categories WHERE category_id = ?""",
        (category_id,)
    )

    response = cursor.fetchone()

    return {
        "id": response[0],
        "name": response[1]
    }

def expense_response(id: int, amount: float, category_id: int, description: str, date_time: str):
    return {
        "id": id,
        "amount": amount,
        "category": get_category(category_id),
        "description": description,
        "date_time": date_time
    }

def create_expense(request):
    now = datetime.now()
    formatted_str = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor = database.db_init()
    database.db_init_tables()

    cursor.execute(
        """INSERT INTO expenses (amount, category_id, description, date_time)
        VALUES (?, ?, ?, ?)""", (request.amount, request.category_id, request.description, formatted_str)
    )

    database.db_commit()

    cursor.execute(
        """SELECT expense_id FROM expenses WHERE amount = ? AND category_id = ? AND description = ? AND date_time = ?""",
        (request.amount, request.category_id, request.description, formatted_str)
    )

    expense_id = cursor.fetchone()
    expense_id = expense_id[0]

    return expense_response(expense_id, request.amount, request.category_id, request.description, formatted_str)

def get_expenses(query, param):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(query, param)

    return cursor.fetchall()
