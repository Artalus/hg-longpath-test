import os
import platform

from pytest import mark

from hgl import Hg
from hgl.init import Const


def test_log(unpack_repo: Hg) -> None:
    x = unpack_repo.out('log -T x')
    assert x == 'xx', 'should contain 2 commits'

@mark.xfail(platform.system() == 'Windows', reason='long paths incompatibility')
def test_status_summary(unpack_repo: Hg) -> None:
    x = unpack_repo.out('status')
    assert not x, 'should not have changes to files'


def test_status_regular(unpack_repo: Hg) -> None:
    x = unpack_repo.out(f'status -A {Const.REGULAR_FILE_NAME}')
    assert x == f'C {Const.REGULAR_FILE_NAME}', 'regular file should be safely committed'


@mark.xfail(platform.system() == 'Windows', reason='long paths incompatibility')
def test_status_long(unpack_repo: Hg) -> None:
    fname = os.path.join(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME).replace('\\', '/')
    x = unpack_repo.out(f'status -A {fname}').replace('\\', '/')
    assert x == f'C {fname}', 'long file should be safely committed'


def test_status_diff(unpack_repo: Hg) -> None:
    x = unpack_repo.out('diff')
    assert not x, 'should be no uncommitted changes'
