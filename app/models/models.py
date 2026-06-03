import uuid
from sqlalchemy import Column, String, Integer, Date, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.database import Base

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