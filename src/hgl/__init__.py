import os
import subprocess
from typing import Optional

class Hg:
    def __init__(self, hg_cmd: str='hg', workdir: Optional[str]=None, user: str='user'):
        self.hg_cmd = hg_cmd
        if not workdir:
            self.cwd = ''
        else:
            self.cwd = f'--cwd "{workdir}"'
        self.user = user


    def do(self, cmd: str) -> None:
        c = f'{self.hg_cmd} {self.cwd} {cmd}'
        rc = os.system(c)
        if rc:
            raise RuntimeError(f'hg failed\ncmd: {c}\nreturn: {rc}')

    def out(self, cmd: str) -> str:
        c = f'{self.hg_cmd} {self.cwd} {cmd}'
        return subprocess.check_output(c, shell=True).decode().strip()

    def commit(self, msg: str) -> None:
        self.do(f'commit -m "{msg}" --config ui.username="{self.user}"')
