from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal, seed_data
from routes import employees

app = FastAPI(
    title="HR Vault API",
    description="Role-based HR app with Auth0, CipherTrust, and Imperva WAF",
    version="0.1.0"
)

# -------------------------------------------------------------------
# CORS — in production this will be locked to your Imperva WAF domain
# -------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------------
# DB init — create tables and seed demo data on first run
# -------------------------------------------------------------------
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

# -------------------------------------------------------------------
# Routers
# -------------------------------------------------------------------
app.include_router(employees.router, prefix="/employees", tags=["employees"])


@app.get("/health", tags=["system"])
def health():
    return {"status": "ok", "service": "hr-vault-backend"}