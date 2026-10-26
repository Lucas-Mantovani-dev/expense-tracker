import database
from datetime import datetime, timedelta
from fastapi import HTTPException

def get_category(category_id: int):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(
        """SELECT * FROM categories WHERE category_id = ?""",
        (category_id,)
    )

    response = cursor.fetchone()

    return {
        "category_id": response[0],
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

    response = cursor.fetchall()
    request_response = []

    for expense in response:
        request_response.append(expense_response(expense[0], expense[1], expense[2], expense[3], expense[4]))

    if not request_response:
        HTTPException(
            status_code=404,
            detail="No expenses found!"
        )
    else:
        return request_response

def get_expense(expense_id):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
    response = cursor.fetchone()

    if not response:
        HTTPException(
            status_code=404,
            detail="Expense not found!"
        )
    else:
        return expense_response(response[0], response[1], response[2], response[3], response[4])

def patch_expense(query, param, expense_id: int):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(query, param)
    database.db_commit()

    return get_expense(expense_id)

def delete_expense(expense_id: int):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
    check_exist = cursor.fetchone()

    if not check_exist:
        HTTPException(
            status_code=404,
            detail="Expense not found!"
        )
    else:
        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        database.db_commit()

        return {
            "expense_id": expense_id,
            "action": "SUCCESSFULLY deleted!"
        }

def get_categories():
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute("SELECT * FROM categories")
    response = cursor.fetchall()
    categories = []

    if not response:
        HTTPException(
            status_code=404,
            detail="No category to be shown..."
        )
    else:
        for category in response:
            categories.append(
                {
                    "category_id": category[0],
                    "name": category[1]
                }
            )

        return categories

def check_category(category_name):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute("SELECT * FROM categories WHERE name = ?", (category_name,))

    response = cursor.fetchone()
    if response:
        return 1
    else:
        return 0

def create_category(category_name):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(
        """INSERT INTO categories (name)
        VALUES (?)""", (category_name,)
    )
    database.db_commit()

    cursor.execute("SELECT * FROM catgeories WHERE category_name = ?", (category_name,))

    response = cursor.fetchone()

    return {
        "category_id": response[0],
        "name": response[1]
    }

def get_month_data(sotm, now):
    database.db_init_tables()
    cursor = database.db_init()
    cursor.execute(
        """SELECT amount FROM expenses WHERE date_time >= ? AND date_time < ?""",
        (sotm, now)
    )

    response = cursor.fetchall()
    amount_count = amount_spent = 0

    for amount in response:
        amount_count += 1
        amount_spent += amount[0]

    return {
        "total_spent": amount_spent,
        "expense_count": amount_count,
        "average_expense": round((amount_spent/amount_count), 2)
    }

def get_week_data(now):
    database.db_init_tables()
    cursor = database.db_init()
    today = datetime.now()
    sunday_start = today - timedelta(days=(today.weekday() + 1) % 7)
    week_start = sunday_start.strftime('%Y-%m-%d')
    
    cursor.execute(
        """SELECT amount FROM expenses WHERE date_time >= ? AND date_time < ?""",
        (week_start, now)
    )

    response = cursor.fetchall()
    amount_count = amount_spent = 0

    for amount in response:
        amount_count += 1
        amount_spent += amount[0]

    return {
        "total_spent": amount_spent,
        "expense_count": amount_count,
        "average_expense": round((amount_spent/amount_count), 2)
    }

def get_summary_data(
        query: str,
        param: tuple,
        sotm, now
):
    database.db_init_tables()
    cursor = database.db_init()

    cursor.execute(query, param)
    response = cursor.fetchall() # LIST WITH AMOUNT TUPLES
    amount_count = amount_spent = 0

    for amount in response:
        amount_count += 1
        amount_spent += amount[0]

    return {
        "filtered_data": {
            "total_spent": amount_spent,
            "expense_count": amount_count,
            "average_expense": round((amount_spent/amount_count), 2)
        },
        "month_data": get_month_data(sotm, now),
        "week_data": get_week_data(now)
    }