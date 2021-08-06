import os
from pytest import mark

from hgl import Hg
from hgl.init import Const

from hgl.utils import windows, filepath


def test_add(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME_2)
    hg.write_file(fname)
    if windows():
        rc = hg.code(f'add {fname}')
        assert rc, 'windows cannot add long paths'
    else:
        hg.do(f'add {fname}')
        x = hg.out(f'status -A {fname}')
        assert x == f'A {fname}', 'long file should be marked for addition'


def test_commit(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    hg.write_file(fname, 'world hello')
    if windows():
        before = hg.out('log -T "{node}"')
        rc = hg.commit_code('another long path')
        assert rc, 'windows cannot commit changes in long paths'
        after = hg.out('log -T "{node}"')
        assert before == after, 'should still contain same commits'
    else:
        hg.commit('another long path')
        x = hg.out('log -T x')
        assert x == 'xxx', 'should contain 3 commits'


def test_strip(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    if windows():
        def long_file_exists() -> bool:
            with hg.chdir():
                return os.path.isfile(filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME))

        before = hg.out('log -T "{node}"')
        assert long_file_exists(), "file exists before strip (of course)"

        rc = hg.code('strip -r .')
        assert rc, 'windows cannot remove long paths during strip'

        assert long_file_exists(), "file should still exist after failed strip"
        after = hg.out('log -T "{node}"')
        assert before == after, 'should still contain same commits'
    else:
        hg.do('strip -r .')
        x = hg.out('log -T x')
        assert x == 'x', 'should contain 1 commit'


def test_move(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    src = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    dst = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME_2)
    # surprisingly, `hg mv` does not fail - yet it reports that "file was marked for deletion"
    hg.do(f'mv {src} {dst}')
    if windows():
        with hg.chdir():
            assert os.path.isfile(src), "source file should remain"
            assert not os.path.isfile(dst), "destination file should not be"
        x = hg.out('status').splitlines()
        assert len(x) < 2, 'hg should not know about move, but can think file was deleted'
    else:
        with hg.chdir():
            assert not os.path.isfile(src), "source file should be removed"
            assert os.path.isfile(dst), "destination file should be created"
        x = hg.out('status').splitlines()
        assert len(x) == 2, 'hg should know about move'
