import os
import uuid
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Form, File, UploadFile
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import settings
from models import Employee
from schemas import EmployeeOut, Token
from utils import get_db, generate_qr_code, create_access_token, get_current_user

if not os.path.exists(settings.UPLOAD_DIR):
    os.makedirs(settings.UPLOAD_DIR)

app = FastAPI()
app.mount("/static", StaticFiles(directory=settings.UPLOAD_DIR), name="static")


@app.post("/employees/", response_model=EmployeeOut)
async def create_employee(
        full_name: str = Form(...),
        email: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
):
    db_employee = db.query(Employee).filter(Employee.email == email).first()
    if db_employee:
        raise HTTPException(status_code=400, detail="Email already registered")

    qr_token = str(uuid.uuid4())
    filename = f"{uuid.uuid4()}_{file.filename}"
    photo_path = os.path.join(settings.UPLOAD_DIR, filename)
    with open(photo_path, "wb") as f:
        f.write(await file.read())

    db_employee = Employee(
        full_name=full_name,
        email=email,
        qr_token=qr_token,
        photo_path=photo_path
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return EmployeeOut(
        id=db_employee.id,
        full_name=db_employee.full_name,
        email=db_employee.email,
        photo_url=f"/uploads/{filename}"
    )


@app.get("/employees/{employee_id}/qr/", response_class=HTMLResponse)
async def get_employee_qr(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    qr_data = generate_qr_code(employee.qr_token)
    html_content = f"""
    <html>
        <head><title>QR Code</title></head>
        <body>
            <h2>QR Code for {employee.full_name}</h2>
            <img src="data:image/png;base64,{qr_data}" alt="QR Code">
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/token/", response_model=Token)
async def login_with_qr(qr_token: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.qr_token == qr_token).first()
    if not employee:
        raise HTTPException(status_code=401, detail="Invalid QR token")

    access_token = create_access_token(data={"sub": employee.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/employees/", response_model=List[EmployeeOut])
async def list_employees(
        request: Request,
        db: Session = Depends(get_db),
        current_user: Employee = Depends(get_current_user)
):
    employees = db.query(Employee).all()

    result = []
    for emp in employees:
        photo_url = None
        if emp.photo_path:
            filename = os.path.basename(emp.photo_path)
            photo_url = f"{request.base_url}static/{filename}"

        result.append(EmployeeOut(
            id=emp.id,
            full_name=emp.full_name,
            email=emp.email,
            photo_url=photo_url
        ))
    return result
