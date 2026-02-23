from sqlalchemy import Column, Integer, String
from database import Base


class Employee(Base):
    __tablename__ = "employees"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    email       = Column(String, unique=True, nullable=False)
    department  = Column(String, nullable=False)
    role        = Column(String, nullable=False)   # admin | hr_manager | employee | auditor
    # These will be encrypted by CipherTrust in Phase 5
    # For now stored as plaintext so the app is fully functional
    salary      = Column(String, nullable=False)   # stored as string (e.g. "85000")
    national_id = Column(String, nullable=False)   # e.g. "123-45-6789"