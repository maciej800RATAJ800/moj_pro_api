from fastapi import FastAPI
from src.middleware.metrics import metrics_middleware, request_count, request_duration
from src.database import init_db
from src.routers.users import router as users_router
import logging

# LOGGING
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# APP
app = FastAPI()

# INIT DB
init_db(load_json_if_empty=False)

# MIDDLEWARE (JEDEN, NIE WIĘCEJ)
app.middleware("http")(metrics_middleware)

# ROUTERS
app.include_router(users_router)

# METRICS ENDPOINT
@app.get("/metrics")
def metrics():
    return {
        "requests": request_count,
        "last_duration_ms": request_duration,
    }

# ROOT
@app.get("/")
def root():
    return {"message": "Hello Maciej"}
