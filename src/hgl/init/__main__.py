import argparse
import os
import shutil
import tarfile

from hgl import Hg
from hgl.init import Const


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    repo = args.repo
    hg = Hg(workdir=repo)
    if os.path.isdir(repo):
        shutil.rmtree(repo)
    os.makedirs(repo)

    hg.do(f'init')

    fname = Const.REGULAR_FILE_NAME
    with hg.chdir():
        with open(fname, 'w') as f:
            f.write("hello world")
    hg.do(f'add {fname}')
    hg.commit(f'add {fname}')

    with hg.chdir():
        os.makedirs(Const.LONG_FOLDER_TREE)
        fname = Const.LONG_FOLDER_TREE + '/' + Const.LONG_FILE_NAME
        with open(fname, 'w') as f:
            f.write("hello world")
    hg.do(f'add {fname}')
    hg.commit(f'add long file')

    with tarfile.open(f'{repo}.tar', "w") as tar:
        tar.add(repo, arcname='.')

if __name__ == '__main__':
    main()
