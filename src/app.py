from fastapi import FastAPI
from src.routers.pdf import router as pdf_router
from src.routers.users import router as users_router
from src.database import Base, engine
from src.models.user import User #WAŻNE (rejestracja modelu)

app = FastAPI(title="My API")

# tworzenie tabel przy starcie aplikacji
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# routery
app.include_router(pdf_router)
app.include_router(users_router)
