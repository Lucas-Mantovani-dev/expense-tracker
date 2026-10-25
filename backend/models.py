from pydantic import BaseModel

class NewExpense(BaseModel):
    amount: float
    category_id: int
    description: str

