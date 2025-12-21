from fastapi import FastAPI, Request
from src.database import init_db
from src.routers.users import router as users_router
import logging
import time

# LOGGING CONFIG
logging.basicConfig(
    filename="api.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

error_logger = logging.getLogger("errors")
fh = logging.FileHandler("errors.log")
fh.setLevel(logging.ERROR)
error_logger.addHandler(fh)

# CREATE APP
app = FastAPI()

# INIT DATABASE (JSON → DB przy pierwszym starcie)
init_db(load_json_if_empty=False)

# LOG REQUESTS
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    try:
        response = await call_next(request)
    except Exception as exc:
        error_logger.error(f"Unhandled error: {exc}")
        raise

    duration = round((time.time() - start) * 1000, 2)
    logging.info(
        f"{request.method} {request.url.path} "
        f"query={dict(request.query_params)} "
        f"status={response.status_code} "
        f"time={duration}ms"
    )
    return response

# ROUTERS
app.include_router(users_router)

# ROOT
@app.get("/")
def root():
    return {"message": "Hello Maciej"}
