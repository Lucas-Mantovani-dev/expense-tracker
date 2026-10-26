from pydantic import BaseModel

class NewExpense(BaseModel):
    amount: float
    category_id: int
    description: str

class PatchExpense(BaseModel):
    amount: float | None = None
    category_id: int | None = None
    description: str | None = None

class NewCategory(BaseModel):
    name: str

