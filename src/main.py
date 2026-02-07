from fastapi import FastAPI
from src import database

app = FastAPI(title="My API")

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/users")
def users():
    return database.get_all_users()
