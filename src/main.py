from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from src.schemas.token import Token
from src.services.auth_service import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    REFRESH_SECRET_KEY,
    ALGORITHM
)

from src.routers import users
from src.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API")
app.include_router(users.router)

# =====================================================
# OAuth2 (dla Swagger Authorize)
# =====================================================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# =====================================================
# GET CURRENT USER (weryfikacja access tokena)
# =====================================================

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {"status": "ok"}


# =====================================================
# REFRESH TOKEN
# =====================================================

@app.post("/refresh")
def refresh_token(refresh_token: str):

    try:
        payload = jwt.decode(
            refresh_token,
            REFRESH_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        new_access_token = create_access_token({"sub": username})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")