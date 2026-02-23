from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:////app/data/hr_vault.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite with FastAPI
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency — yields a DB session, always closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def seed_data(db):
    """Insert demo employees if the table is empty."""
    from models import Employee
    if db.query(Employee).count() > 0:
        return

    employees = [
        Employee(name="Alice Admin",   email="alice@hrvault.dev",   department="IT",        role="admin",      salary="120000", national_id="111-22-3333"),
        Employee(name="Harry HR",      email="harry@hrvault.dev",   department="HR",        role="hr_manager", salary="95000",  national_id="444-55-6666"),
        Employee(name="Eve Employee",  email="eve@hrvault.dev",     department="Finance",   role="employee",   salary="72000",  national_id="777-88-9999"),
        Employee(name="Aiden Auditor", email="aiden@hrvault.dev",   department="Compliance",role="auditor",    salary="88000",  national_id="000-11-2222"),
        Employee(name="Bob Dev",       email="bob@hrvault.dev",     department="IT",        role="employee",   salary="78000",  national_id="333-44-5555"),
    ]
    db.add_all(employees)
    db.commit()