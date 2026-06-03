from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

class StudentCreate(BaseModel):
    name: str
    course_name: str
    total_fee: int

class StudentOut(StudentCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class StudentPaymentCreate(BaseModel):
    student_id: UUID
    amount: int
    payment_date: date
    payment_method: str
    note: Optional[str] = None

class StudentPaymentOut(StudentPaymentCreate):
    id: UUID
    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    client_name: str
    project_name: str
    total_amount: int

class ClientOut(ClientCreate):
    id: UUID
    created_at: datetime
    class Config:
        from_attributes = True

class ClientPaymentCreate(BaseModel):
    client_id: UUID
    amount: int
    payment_date: date

class ClientPaymentOut(ClientPaymentCreate):
    id: UUID
    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    title: str
    amount: int
    category: str
    expense_date: date

class ExpenseOut(ExpenseCreate):
    id: UUID
    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    name: str
    role: str
    salary: int

class EmployeeOut(EmployeeCreate):
    id: UUID
    class Config:
        from_attributes = True

class SalaryCreate(BaseModel):
    employee_id: UUID
    amount: int
    payment_date: date
    status: Optional[str] = "Pending"

class SalaryOut(SalaryCreate):
    id: UUID
    class Config:
        from_attributes = True