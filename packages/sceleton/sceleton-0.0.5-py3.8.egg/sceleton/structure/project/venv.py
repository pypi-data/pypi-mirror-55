import subprocess
import os

from . import python_v
from . import VersionError

def init(project_path):
    venv = os.path.join(project_path, "venv")

    if not os.path.exists(venv):
        os.makedirs(venv)

    version = python_v()

    if version < (3, 0, 0):
        subprocess.run(["python3",  "-m", "venv", venv, "--without-pip"])
    elif (3, 0, 0) < version < (3, 7, 0):
        raise VersionError("Minimum acceptable version is 3.7.1, but found {}.{}.{}".format(version.major, version.minor, version.micro))
    else:
        subprocess.run(["python", "-m", "venv", venv, "--without-pip"])
