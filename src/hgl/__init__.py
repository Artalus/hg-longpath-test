import os
import subprocess
import contextlib
from typing import Iterator, Optional

class Hg:
    def __init__(self, hg_cmd: str='hg', workdir: Optional[str]=None, user: str='user'):
        self.hg_cmd = hg_cmd
        self.workdir = workdir
        self.user = user


    def up(self, commit: Optional[str]=None) -> 'Hg':
        cmd = 'up'
        if commit:
            cmd += ' '+commit
        self.do(cmd)
        return self


    def code(self, cmd: str) -> int:
        with self.chdir():
            c = f'{self.hg_cmd} {cmd}'
            return os.system(c)


    def do(self, cmd: str) -> None:
        rc = self.code(cmd)
        if rc:
            raise RuntimeError(f'{self.hg_cmd} failed\ncmd: {cmd}\nreturn: {rc}')

    def out(self, cmd: str) -> str:
        with self.chdir():
            c = f'{self.hg_cmd} {cmd}'
            return subprocess.check_output(c, shell=True).decode().strip()

    # TODO: write username once on init
    def __commit_cmd(self, msg: str) -> str:
        return f'commit -m "{msg}" --config ui.username="{self.user}"'
    def commit(self, msg: str) -> None:
        self.do(self.__commit_cmd(msg))
    def commit_code(self, msg: str) -> int:
        return self.code(self.__commit_cmd(msg))


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


    def write_file(self, path: str, content: str='hello world') -> None:
        with self.chdir():
            dirs, _ = os.path.split(path)
            if dirs and not os.path.isdir(dirs):
                os.makedirs(dirs)
            with open(path, 'w') as f:
                f.write(content)


    def is_exe(self) -> bool:
        return ' ' not in self.hg_cmd
