import os
import platform


def filepath(*args: str) -> str:
    return os.path.join(*args).replace('\\', '/')

def windows() -> bool:
    return platform.system() == 'Windows'
