from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List

from app.database import get_db
from app.models.models import Student, StudentPayment
from app.schemas.schemas import StudentCreate, StudentOut, StudentPaymentCreate, StudentPaymentOut

router = APIRouter()

@router.post("/students", response_model=StudentOut, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(**student.model_dump())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@router.get("/students", response_model=List[StudentOut], tags=["Students"])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@router.get("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def get_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/students/{student_id}", response_model=StudentOut, tags=["Students"])
def update_student(student_id: UUID, updated: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    for key, value in updated.model_dump().items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

@router.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: UUID, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully"}

@router.post("/student-payments", response_model=StudentPaymentOut, tags=["Student Payments"])
def create_student_payment(payment: StudentPaymentCreate, db: Session = Depends(get_db)):
    new_payment = StudentPayment(**payment.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

@router.get("/student-payments", response_model=List[StudentPaymentOut], tags=["Student Payments"])
def get_student_payments(db: Session = Depends(get_db)):
    return db.query(StudentPayment).all()

@router.get("/student-payments/{payment_id}", response_model=StudentPaymentOut, tags=["Student Payments"])
def get_student_payment(payment_id: UUID, db: Session = Depends(get_db)):
    payment = db.query(StudentPayment).filter(StudentPayment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@router.delete("/student-payments/{payment_id}", tags=["Student Payments"])
def delete_student_payment(payment_id: UUID, db: Session = Depends(get_db)):
    payment = db.query(StudentPayment).filter(StudentPayment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"message": "Payment deleted successfully"}