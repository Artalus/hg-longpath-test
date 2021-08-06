from pytest import mark

from hgl import Hg
from hgl.init import Const

from hgl.utils import windows, filepath


def test_log(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    x = hg.out('log -T x')
    assert x == 'xx', 'should contain 2 commits'

def test_status_summary(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    x = hg.out('status')
    if windows():
        assert x, 'windows detects some changes to long path files'
    else:
        assert not x, 'should not have changes to files'


def test_status_regular(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    x = hg.out(f'status -A {Const.REGULAR_FILE_NAME}')
    assert x == f'C {Const.REGULAR_FILE_NAME}', 'regular file should be safely committed'


def test_status_long(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    x = hg.out(f'status -A {fname}').replace('\\', '/')
    if windows():
        assert x == f'! {fname}', 'windows does not see long path and considers it deleted'
    else:
        assert x == f'C {fname}', 'long file should be safely committed'


def test_status_diff(unpack_repo: str) -> None:
    hg = Hg(workdir=unpack_repo)
    x = hg.out('diff')
    assert not x, 'should be no uncommitted changes'
