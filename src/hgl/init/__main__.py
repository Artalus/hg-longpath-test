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
    hg.write_file(fname)
    hg.do(f'add {fname}')
    hg.commit(f'add {fname}')

    fname = Const.LONG_FOLDER_TREE + '/' + Const.LONG_FILE_NAME
    hg.write_file(fname)
    hg.do(f'add {fname}')
    hg.commit(f'add long file')

    with tarfile.open(f'{repo}.tar', "w") as tar:
        tar.add(repo, arcname='.')

if __name__ == '__main__':
    main()
