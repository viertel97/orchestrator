import os

from loguru import logger

from helper.deployment_helper import deploy_to_server_with_git

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)

APPLICATION_PATH = "orchestrator"

if __name__ == "__main__":
    deploy_to_server_with_git(
        application_path=APPLICATION_PATH,
    )
    logger.info("done")


