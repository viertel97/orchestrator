import hmac

from fastapi import APIRouter, Request
from fastapi import HTTPException
from quarter_lib.akeyless import get_secrets
from quarter_lib.logging import setup_logging

from helper.deployment_helper import update_application

logger = setup_logging(__file__)

router = APIRouter()

webhook_secret = get_secrets(["github/webhook_secret"])


@logger.catch
@router.post("/{application}")
async def deploy(application: str, request: Request):
    if not request.headers["X-Hub-Signature-256"]:
        raise HTTPException(status_code=403, detail="x-hub-signature-256 header is missing!")
    logger.info("received request for application: %s", application)
    body = await request.body()
    expected_signature = "sha256=" + hmac.new(webhook_secret.encode(), body, "sha256").hexdigest()
    signature = request.headers["X-Hub-Signature-256"]
    if not hmac.compare_digest(expected_signature, signature):
        logger.error("signature mismatch")
        return
    update_application(application)
    logger.info("done")
