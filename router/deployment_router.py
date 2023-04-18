from fastapi import APIRouter
from quarter_lib.logging import setup_logging

from helper.deployment_helper import upadte_application

logger = setup_logging(__file__)

router = APIRouter()


@logger.catch
@router.post("/{application}")
async def deploy(application: str):
    logger.info(f"{application}")
    upadte_application(application)
