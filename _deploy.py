from helper.deployment_helper import deploy_to_server_with_git
from helper.logging_helper import setup_logging

logger = setup_logging(__file__)

APPLICATION_PATH = "orchestrator"

if __name__ == "__main__":
    deploy_to_server_with_git(
        application_path=APPLICATION_PATH,
    )
    logger.info("done")
