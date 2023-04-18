import subprocess

from quarter_lib.logging import setup_logging

logger = setup_logging(__file__)

PM2_PATH = "/home/pi/.config/nvm/versions/node/v16.18.0/bin"


def generate_command(command, application_path):
    temp_cmd = "cd " + application_path + "; " + command
    return temp_cmd


def generate_pm2_command(command, application_name, pm2_path=PM2_PATH):
    temp_cmd = "cd " + pm2_path + "; ./pm2 " + command + " " + application_name
    return temp_cmd


def generate_start_pm2_command(application_name, pm2_path=PM2_PATH):
    temp_cmd = "cd " + pm2_path + "; ./pm2 start /home/pi/code/" + application_name + "/process.json"
    return temp_cmd


def generate_update_command(application_path: object, requirements_file: object = "requirements.txt"):
    temp_cmd = "{absolute_path}/venv/bin/pip3.9 install -r {absolute_path}/{requirements_file} --upgrade".format(
        absolute_path=application_path, requirements_file=requirements_file
    )
    return temp_cmd


def ssh_command(ssh, command):
    logger.info(command)
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    for line in iter(ssh_stdout.readline, ""):
        print(line.encode("utf-8"), end="")
    for line in iter(ssh_stderr.readline, ""):
        print(line.encode("utf-8"), end="")


def bash_command(command):
    logger.info("command: " + command)
    return subprocess.check_output(command, shell=True).decode("utf-8").strip()
