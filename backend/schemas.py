from pydantic import BaseModel
from typing import Optional


class EmployeePublic(BaseModel):
    """Fields safe to return to any authenticated user."""
    id:         int
    name:       str
    email:      str
    department: str
    role:       str

    model_config = {"from_attributes": True}


class EmployeeMasked(EmployeePublic):
    """Auditor view — sensitive fields are masked."""
    email:       str  # will be masked at response time
    salary:      str  # "$***,***"
    national_id: str  # "***-**-XXXX"


class EmployeeFull(EmployeePublic):
    """HR Manager / Admin view — all fields visible (after MFA for sensitive)."""
    salary:      str
    national_id: str