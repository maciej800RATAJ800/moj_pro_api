import time
import logging
from fastapi import Request
from collections import defaultdict

logger = logging.getLogger("monitoring")

# LICZNIKI
request_count = defaultdict(int)
request_duration = {}

async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = round((time.perf_counter() - start) * 1000, 2)
    key = f"{request.method} {request.url.path}"

    request_count[key] += 1
    request_duration[key] = duration_ms

    logger.info(
        "method=%s path=%s status=%d duration=%.2fms count=%d",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_count[key],
    )

    return response
