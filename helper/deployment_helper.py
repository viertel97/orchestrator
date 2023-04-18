import paramiko
from quarter_lib.akeyless import get_secrets
from quarter_lib.logging import setup_logging

from helper.command_helper import generate_pm2_command, generate_command, generate_update_command, \
    generate_start_pm2_command, run_ssh_command, run_bash_command

logger = setup_logging(__file__)

PI_PYTHON_PATH = "/home/pi/code"
PM2_PATH = "/home/pi/.config/nvm/versions/node/v16.18.0/bin"
PM2_PATH_NOTES = "/home/pi/.config/nvm/versions/node/v8.17.0/bin"


def update_application(application):
    run_bash_command(generate_pm2_command("delete", application))
    absolute_application_path = PI_PYTHON_PATH + "/" + application
    run_bash_command(generate_command("git pull", absolute_application_path))

    run_bash_command(
        "{update_command}".format(
            update_command=generate_update_command(absolute_application_path),
        ),
    )
    run_bash_command("sleep 5")
    run_bash_command(
        "{start_command}".format(
            start_command=generate_start_pm2_command(application),
        ),
    )


def deploy_to_server_with_git(application_path, skip_update=False):
    server, username, password = get_secrets(
        ['raspberrypi/address', 'raspberrypi/username', 'raspberrypi/password'])

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    run_ssh_command(ssh, generate_pm2_command("delete", application_path))
    run_ssh_command(ssh, generate_pm2_command("delete", "pagekite"))
    absolute_application_path = PI_PYTHON_PATH + "/" + application_path
    run_ssh_command(ssh, generate_command("git pull", absolute_application_path))

    if not skip_update:
        run_ssh_command(
            ssh,
            "{update_command}".format(
                update_command=generate_update_command(absolute_application_path),
            ),
        )
    run_ssh_command(ssh, "sleep 5")
    run_ssh_command(
        ssh,
        "{start_command}".format(
            start_command=generate_start_pm2_command(application_path),
        ),
    )

    ssh.close()
