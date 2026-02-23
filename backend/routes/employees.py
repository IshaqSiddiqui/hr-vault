from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Employee
from schemas import EmployeePublic, EmployeeMasked, EmployeeFull
from auth import verify_token, get_role

router = APIRouter()


def mask_employee(emp: Employee) -> EmployeeMasked:
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
# GET /employees — public fields, requires valid JWT
# -------------------------------------------------------------------
@router.get("/", response_model=list[EmployeePublic])
def list_employees(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)   # ← Phase 2: JWT required
):
    return db.query(Employee).all()


# -------------------------------------------------------------------
# GET /employees/{id} — single employee public fields
# -------------------------------------------------------------------
@router.get("/{employee_id}", response_model=EmployeePublic)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


# -------------------------------------------------------------------
# GET /employees/{id}/sensitive — salary + national ID
# Phase 2: requires valid JWT
# Phase 3: will enforce role (admin/hr_manager only)
# Phase 4: will enforce acr=mfa step-up
# -------------------------------------------------------------------
@router.get("/{employee_id}/sensitive")
def get_sensitive(
    employee_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    emp = db.query(Employee).filter(Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    role = get_role(payload)

    # Auditor gets masked data
    if role == "auditor":
        return {
            "salary":      "$***,***",
            "national_id": f"***-**-{emp.national_id[-4:]}",
        }

    # Employee can only see their own record and never sees sensitive fields
    if role == "employee":
        raise HTTPException(status_code=403, detail="Access denied")

    # Admin and HR Manager see full data (MFA enforcement added in Phase 4)
    return {
        "salary":      emp.salary,
        "national_id": emp.national_id,
    }