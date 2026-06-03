from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models.models import Employee, Salary
from app.schemas.schemas import EmployeeCreate, EmployeeOut, SalaryCreate, SalaryOut

router = APIRouter()

@router.post("/employees", response_model=EmployeeOut, tags=["Employees"])
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@router.get("/employees", response_model=List[EmployeeOut], tags=["Employees"])
def get_all_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

@router.get("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"])
def get_employee(employee_id: UUID, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@router.put("/employees/{employee_id}", response_model=EmployeeOut, tags=["Employees"])
def update_employee(employee_id: UUID, updated: EmployeeCreate, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    for key, value in updated.model_dump().items():
        setattr(employee, key, value)
    db.commit()
    db.refresh(employee)
    return employee

@router.delete("/employees/{employee_id}", tags=["Employees"])
def delete_employee(employee_id: UUID, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(employee)
    db.commit()
    return {"message": "Employee deleted successfully"}

@router.post("/salaries", response_model=SalaryOut, tags=["Salaries"])
def create_salary(salary: SalaryCreate, db: Session = Depends(get_db)):
    new_salary = Salary(**salary.model_dump())
    db.add(new_salary)
    db.commit()
    db.refresh(new_salary)
    return new_salary

@router.get("/salaries", response_model=List[SalaryOut], tags=["Salaries"])
def get_all_salaries(db: Session = Depends(get_db)):
    return db.query(Salary).all()