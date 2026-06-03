from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models.models import Expense
from app.schemas.schemas import ExpenseCreate, ExpenseOut

router = APIRouter()

@router.post("/expenses", response_model=ExpenseOut, tags=["Expenses"])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = Expense(**expense.model_dump())
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get("/expenses", response_model=List[ExpenseOut], tags=["Expenses"])
def get_all_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@router.get("/expenses/{expense_id}", response_model=ExpenseOut, tags=["Expenses"])
def get_expense(expense_id: UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/expenses/{expense_id}", response_model=ExpenseOut, tags=["Expenses"])
def update_expense(expense_id: UUID, updated: ExpenseCreate, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for key, value in updated.model_dump().items():
        setattr(expense, key, value)
    db.commit()
    db.refresh(expense)
    return expense

@router.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: UUID, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}