import os
from  pathlib import Path
import platform
import sys


def filepath(*args: str) -> str:
    return os.path.join(*args).replace('\\', '/')

def windows() -> bool:
    return platform.system() == 'Windows'

def possible_hg_commands() -> list[str]:
    if not windows():
        return ['hg']
    python_dir = Path(sys.executable).parent
    if python_dir.name == 'Scripts':
        # we are likely in virtualenv, and hg will be right here
        scripts_dir = python_dir
    else:
        scripts_dir = python_dir / 'Scripts'
    hg_script =  scripts_dir / 'hg'
    cmd = f'{sys.executable} {hg_script}'
    return ['hg.exe', cmd]
