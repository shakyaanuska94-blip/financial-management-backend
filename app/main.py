from fastapi import FastAPI
from mangum import Mangum
from app.database import engine, Base
from app.routes import students, clients, expenses, employees

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Financial Management Backend System",
    description="Backend for managing student payments, SaaS clients, expenses, and employee salaries.",
    version="1.0.0"
)

app.include_router(students.router)
app.include_router(clients.router)
app.include_router(expenses.router)
app.include_router(employees.router)

@app.get("/", tags=["Health"])
def root():
    return {"message": "Financial Management API is running!"}

handler = Mangum(app)