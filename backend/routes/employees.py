from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
from schemas import EmployeePublic, EmployeeMasked, EmployeeFull

router = APIRouter()


def mask_employee(emp: Employee) -> EmployeeMasked:
    """Return an employee record with sensitive fields masked (auditor view)."""
    return EmployeeMasked(
        id=emp.id,
        name=emp.name,
        email=emp.email[:2] + "***@***.***",
        department=emp.department,
        role=emp.role,
        salary="$***,***",
        national_id=f"***-**-{emp.national_id[-4:]}",
    )


# -------------------------------------------------------------------
# GET /employees  — list all employees (public fields only for now)
# Auth + RBAC will be added in Phase 2 & 3
# -------------------------------------------------------------------
@router.get("/", response_model=list[EmployeePublic])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# -------------------------------------------------------------------
# GET /employees/{id}  — single employee (public fields)
# -------------------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeePublic)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# -------------------------------------------------------------------
# GET /employees/{id}/sensitive  — salary + national ID
# Phase 3: will enforce role check
# Phase 4: will enforce MFA step-up via Auth0 acr claim
# -------------------------------------------------------------------
@router.get("/{employee_id}/sensitive")
def get_sensitive(employee_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    # TODO Phase 3 — enforce role
    # TODO Phase 4 — enforce acr=mfa
    return {
        "salary":      emp.salary,
        "national_id": emp.national_id,
    }