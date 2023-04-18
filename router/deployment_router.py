from fastapi import APIRouter

from helper.deployment_helper import upadte_application
from helper.logging_helper import setup_logging

logger = setup_logging(__file__)

router = APIRouter()


@logger.catch
@router.post("/{application}")
async def deploy(application: str):
    logger.info(f"{application}")
    upadte_application(application)
