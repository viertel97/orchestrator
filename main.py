import platform
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from helper.logging_helper import setup_logging
from helper.network_helper import log_request_info
from router import (
    deployment_router,
)

logger = setup_logging(__file__)

controllers = [
    deployment_router,
]

app = FastAPI(debug=True)
[app.include_router(controller.router, dependencies=[Depends(log_request_info)]) for controller in controllers]


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == "__main__":
    if platform.system() == "Windows":
        uvicorn.run(f"{Path(__file__).stem}:app", host="0.0.0.0", reload=True, port=9999)
    else:
        uvicorn.run(app, host="0.0.0.0", port=9999)
