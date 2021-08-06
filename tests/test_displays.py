from typing import Callable
from pytest import mark

from hgl import Hg
from hgl.init import Const

from hgl.utils import windows, filepath, possible_hg_commands


HgTest = Callable[[str, list[str]], None]
def multiple_hg(func: HgTest) -> HgTest:
    return mark.parametrize("hg_cmd", possible_hg_commands())(func)


@multiple_hg
def test_log(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    x = hg.out('log -T x')
    assert x == 'xx', 'should contain 2 commits'

@multiple_hg
def test_status_summary(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    x = hg.out('status')
    if windows() and hg.is_exe():
        assert x, 'windows detects some changes to long path files'
    else:
        assert not x, 'should not have changes to files'


@multiple_hg
def test_status_regular(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    x = hg.out(f'status -A {Const.REGULAR_FILE_NAME}')
    assert x == f'C {Const.REGULAR_FILE_NAME}', 'regular file should be safely committed'


@multiple_hg
def test_status_long(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    x = hg.out(f'status -A {fname}').replace('\\', '/')
    if windows() and hg.is_exe():
        assert x == f'! {fname}', 'windows does not see long path and considers it deleted'
    else:
        assert x == f'C {fname}', 'long file should be safely committed'


@multiple_hg
def test_diff(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    x = hg.out('diff')
    assert not x, 'should be no uncommitted changes'
