import os
import subprocess
import contextlib
from typing import Iterator, Optional

class Hg:
    def __init__(self, hg_cmd: str='hg', workdir: Optional[str]=None, user: str='user'):
        self.hg_cmd = hg_cmd
        self.workdir = workdir
        self.user = user


    def do(self, cmd: str) -> None:
        with self.chdir():
            c = f'{self.hg_cmd} {cmd}'
            rc = os.system(c)
        if rc:
            raise RuntimeError(f'hg failed\ncmd: {c}\nreturn: {rc}')

    def out(self, cmd: str) -> str:
        with self.chdir():
            c = f'{self.hg_cmd} {cmd}'
            return subprocess.check_output(c, shell=True).decode().strip()

    def commit(self, msg: str) -> None:
        self.do(f'commit -m "{msg}" --config ui.username="{self.user}"')

    @contextlib.contextmanager
    def chdir(self) -> Iterator[None]:
        if not self.workdir:
            return

        cwd = os.getcwd()
        os.chdir(self.workdir)
        try:
            yield
        finally:
            os.chdir(cwd)
