import os

from fastapi import APIRouter
from loguru import logger

from helper.deployment_helper import upadte_application

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

router = APIRouter()


@logger.catch
@router.post("/{application}")
async def deploy(application: str):
    logger.info(f"{application}")
    upadte_application(application)
