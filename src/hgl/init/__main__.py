import argparse
import os
import shutil
import tarfile

from hgl import Hg


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

    fname = 'file.txt'
    with open(f'{repo}/{fname}', 'w') as f:
        f.write("hello world")
    hg.do(f'add {fname}')
    hg.commit(f'add {fname}')

    with tarfile.open(f'{repo}.tgz', "w:gz") as tar:
        tar.add(repo, arcname='.')

if __name__ == '__main__':
    main()
