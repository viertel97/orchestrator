import os
import subprocess

from loguru import logger

PM2_PATH = "/home/pi/.config/nvm/versions/node/v16.18.0/bin"

logger.add(
    os.path.join(os.path.dirname(os.path.abspath(__file__)) + "/logs/" + os.path.basename(__file__) + ".log"),
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    backtrace=True,
    diagnose=True,
)


def generate_command(command, application_path):
    return "cd " + application_path + "; " + command


def generate_pm2_command(command, application_name, pm2_path=PM2_PATH):
    return "cd " + pm2_path + "; ./pm2 " + command + " " + application_name


def generate_start_pm2_command(application_name, pm2_path=PM2_PATH):
    return "cd " + pm2_path + "; ./pm2 start /home/pi/code/" + application_name + "/process.json"


def generate_update_command(application_path: object, requirements_file: object = "requirements.txt") -> object:
    return "{absolute_path}/venv/bin/pip3.9 install -r {absolute_path}/{requirements_file} --upgrade".format(
        absolute_path=application_path, requirements_file=requirements_file
    )


def ssh_command(ssh, command):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    for line in iter(ssh_stdout.readline, ""):
        print(line.encode("utf-8"), end="")
    for line in iter(ssh_stderr.readline, ""):
        print(line.encode("utf-8"), end="")


def cmd(command):
    return subprocess.check_output(command, shell=True).decode("utf-8").strip()
