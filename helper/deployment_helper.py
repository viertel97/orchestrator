import os

import paramiko
from loguru import logger
from quarter_lib.akeyless import get_secrets

from helper.ssh_helper import cmd, generate_pm2_command, generate_command, generate_update_command, \
    generate_start_pm2_command, ssh_command

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)
SERVER, USERNAME, PASSWORD = get_secrets(
    ['raspberrypi/address', 'raspberrypi/username', 'raspberrypi/password'])

PI_PYTHON_PATH = "/home/pi/code"
PM2_PATH = "/home/pi/.config/nvm/versions/node/v16.18.0/bin"
PM2_PATH_NOTES = "/home/pi/.config/nvm/versions/node/v8.17.0/bin"


def upadte_application(application):
    cmd(generate_pm2_command("delete", application))
    absolute_application_path = PI_PYTHON_PATH + "/" + application
    cmd(generate_command("git pull", absolute_application_path))

    cmd(
        "{update_command}; sleep 5; {update_command_custom}".format(
            update_command=generate_update_command(absolute_application_path),
            update_command_custom=generate_update_command(absolute_application_path, "requirements_custom.txt"),
        ),
    )
    cmd("sleep 5;")
    cmd(
        "{start_command}".format(
            start_command=generate_start_pm2_command(application),
        ),
    )


def deploy_to_server_with_git(application_path, skip_update=False):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER, username=USERNAME, password=PASSWORD)
    ssh_command(ssh, generate_pm2_command("delete", application_path))
    ssh_command(ssh, "git pull")
    absolute_application_path = PI_PYTHON_PATH + "/" + application_path

    if not skip_update:
        ssh_command(
            ssh,
            "{update_command}; sleep 5; {update_command_custom}".format(
                update_command=generate_update_command(absolute_application_path),
                update_command_custom=generate_update_command(absolute_application_path, "requirements_custom.txt"),
            ),
        )
    ssh_command(ssh, "sleep 5;")
    ssh_command(
        ssh,
        "{start_command}".format(
            start_command=generate_start_pm2_command(application_path),
        ),
    )

    ssh.close()
