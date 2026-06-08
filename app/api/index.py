import os
import uuid
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from sqlalchemy import create_engine, Column, String, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID as PyUUID
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Models
class Student(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    course_name = Column(String, nullable=False)
    total_fee = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StudentPayment(Base):
    __tablename__ = "student_payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)
    payment_method = Column(String, nullable=False)
    note = Column(Text, nullable=True)

class Client(Base):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_name = Column(String, nullable=False)
    project_name = Column(String, nullable=False)
    total_amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ClientPayment(Base):
    __tablename__ = "client_payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    category = Column(String, nullable=False)
    expense_date = Column(Date, nullable=False)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)

class Salary(Base):
    __tablename__ = "salaries"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=False)
    amount = Column(Integer, nullable=False)
    payment_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, default="Pending")

Base.metadata.create_all(bind=engine)

# Schemas
class StudentCreate(BaseModel):
    name: str
    course_name: str
    total_fee: int

class StudentOut(StudentCreate):
    id: PyUUID
    created_at: datetime
    class Config:
        from_attributes = True

class StudentPaymentCreate(BaseModel):
    student_id: PyUUID
    amount: int
    payment_date: date
    payment_method: str
    note: Optional[str] = None

class StudentPaymentOut(StudentPaymentCreate):
    id: PyUUID
    class Config:
        from_attributes = True

class ClientCreate(BaseModel):
    client_name: str
    project_name: str
    total_amount: int

class ClientOut(ClientCreate):
    id: PyUUID
    created_at: datetime
    class Config:
        from_attributes = True

class ClientPaymentCreate(BaseModel):
    client_id: PyUUID
    amount: int
    payment_date: date

class ClientPaymentOut(ClientPaymentCreate):
    id: PyUUID
    class Config:
        from_attributes = True

class ExpenseCreate(BaseModel):
    title: str
    amount: int
    category: str
    expense_date: date

class ExpenseOut(ExpenseCreate):
    id: PyUUID
    class Config:
        from_attributes = True

class EmployeeCreate(BaseModel):
    name: str
    role: str
    salary: int

class EmployeeOut(EmployeeCreate):
    id: PyUUID
    class Config:
        from_attributes = True

class SalaryCreate(BaseModel):
    employee_id: PyUUID
    amount: int
    payment_date: date
    status: Optional[str] = "Pending"

class SalaryOut(SalaryCreate):
    id: PyUUID
    class Config:
        from_attributes = True

# App
app = FastAPI(title="Financial Management Backend System", version="1.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"message": "Financial Management API is running!"}

# Student routes
@app.post("/students", response_model=StudentOut, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new = Student(**student.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/students", response_model=List[StudentOut], tags=["Students"])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def get_student(student_id: PyUUID, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.id == student_id).first()
    if not s: raise HTTPException(404, "Student not found")
    return s

@app.put("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def update_student(student_id: PyUUID, updated: StudentCreate, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.id == student_id).first()
    if not s: raise HTTPException(404, "Student not found")
    for k, v in updated.model_dump().items(): setattr(s, k, v)
    db.commit(); db.refresh(s)
    return s

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: PyUUID, db: Session = Depends(get_db)):
    s = db.query(Student).filter(Student.id == student_id).first()
    if not s: raise HTTPException(404, "Student not found")
    db.delete(s); db.commit()
    return {"message": "Deleted"}

@app.post("/student-payments", response_model=StudentPaymentOut, tags=["Student Payments"])
def create_student_payment(p: StudentPaymentCreate, db: Session = Depends(get_db)):
    new = StudentPayment(**p.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/student-payments", response_model=List[StudentPaymentOut], tags=["Student Payments"])
def get_student_payments(db: Session = Depends(get_db)):
    return db.query(StudentPayment).all()

# Client routes
@app.post("/clients", response_model=ClientOut, tags=["Clients"])
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new = Client(**client.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/clients", response_model=List[ClientOut], tags=["Clients"])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@app.get("/clients/{client_id}", response_model=ClientOut, tags=["Clients"])
def get_client(client_id: PyUUID, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.id == client_id).first()
    if not c: raise HTTPException(404, "Client not found")
    return c

@app.delete("/clients/{client_id}", tags=["Clients"])
def delete_client(client_id: PyUUID, db: Session = Depends(get_db)):
    c = db.query(Client).filter(Client.id == client_id).first()
    if not c: raise HTTPException(404, "Client not found")
    db.delete(c); db.commit()
    return {"message": "Deleted"}

@app.post("/client-payments", response_model=ClientPaymentOut, tags=["Client Payments"])
def create_client_payment(p: ClientPaymentCreate, db: Session = Depends(get_db)):
    new = ClientPayment(**p.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/client-payments", response_model=List[ClientPaymentOut], tags=["Client Payments"])
def get_client_payments(db: Session = Depends(get_db)):
    return db.query(ClientPayment).all()

# Expense routes
@app.post("/expenses", response_model=ExpenseOut, tags=["Expenses"])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    new = Expense(**expense.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/expenses", response_model=List[ExpenseOut], tags=["Expenses"])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()

@app.delete("/expenses/{expense_id}", tags=["Expenses"])
def delete_expense(expense_id: PyUUID, db: Session = Depends(get_db)):
    e = db.query(Expense).filter(Expense.id == expense_id).first()
    if not e: raise HTTPException(404, "Expense not found")
    db.delete(e); db.commit()
    return {"message": "Deleted"}

# Employee routes
@app.post("/employees", response_model=EmployeeOut, tags=["Employees"])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new = Employee(**employee.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/employees", response_model=List[EmployeeOut], tags=["Employees"])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@app.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: PyUUID, db: Session = Depends(get_db)):
    e = db.query(Employee).filter(Employee.id == employee_id).first()
    if not e: raise HTTPException(404, "Employee not found")
    db.delete(e); db.commit()
    return {"message": "Deleted"}

@app.post("/salaries", response_model=SalaryOut, tags=["Salaries"])
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db)):
    new = Salary(**salary.model_dump())
    db.add(new); db.commit(); db.refresh(new)
    return new

@app.get("/salaries", response_model=List[SalaryOut], tags=["Salaries"])
def get_salaries(db: Session = Depends(get_db)):
    return db.query(Salary).all()

handler = Mangum(app)