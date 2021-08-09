from typing import Callable
import os

import pytest
from pytest import mark

from hgl import Hg
from hgl.init import Const
from hgl.utils import filepath, possible_hg_commands, windows


HgTest = Callable[..., None]
def multiple_hg(func: HgTest) -> HgTest:
    return mark.parametrize("hg_cmd", possible_hg_commands())(func)


@pytest.fixture(scope='function')
def clonedir(tmpdir_factory: pytest.TempdirFactory) -> str:
    return ("%s" % tmpdir_factory.mktemp("clone")).replace("\\", "/")


@multiple_hg
def test_clone_noupdate(unpack_repo: str, clonedir: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=clonedir, hg_cmd=hg_cmd)

    hg.do(f'clone {unpack_repo} ./ --noupdate')

    with hg.chdir():
        assert os.path.isdir('.hg'), "hg dir should exist"
        assert os.path.isdir('.hg/store'), "hg data should exist"
        assert os.path.isfile('.hg/hgrc'), "hg config should exist"

    x = hg.out('status -A')
    assert not x, "no files should be reported by hg"


@multiple_hg
def test_clone_noupdate_update(unpack_repo: str, clonedir: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=clonedir, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    def long_file_exists() -> bool:
        with hg.chdir():
            return os.path.isfile(fname)

    hg.do(f'clone {unpack_repo} ./ --noupdate')
    if windows() and hg.is_exe():
        rc = hg.code('up')
        assert rc, "windows cannot update to commit with long paths"
        assert not long_file_exists(), "long file does not exist"
    else:
        hg.up()
        assert long_file_exists(), "long file should exist"
    x = hg.out('status')
    assert not x, "clone should be intact"


@multiple_hg
def test_clone(unpack_repo: str, clonedir: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=clonedir, hg_cmd=hg_cmd)

    if windows() and hg.is_exe():
        rc = hg.code(f'clone {unpack_repo} ./')
        assert rc, "windows cannot create files after clone"
        with hg.chdir():
            assert os.path.isdir('.hg/store'), "hg data should exist"
            fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
            assert not os.path.isfile(fname), "but long file cannot be created"
    else:
        hg.do(f'clone {unpack_repo} ./')
        with hg.chdir():
            fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
            assert os.path.isfile(fname), "long file should exist"

    x = hg.out('status')
    assert not x, "clone should be intact"


@multiple_hg
def test_pull(unpack_repo: str, clonedir: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=clonedir, hg_cmd=hg_cmd)

    hg.do('init')

    x = hg.out('log -T x')
    assert len(x) == 0, "no commits after initialization"

    x = hg.out('status -A')
    assert not x, "no files should be reported by hg"

    hg.do(f'pull "{unpack_repo}"')

    x = hg.out('log -T x')
    assert len(x) == 2, "repo should have 2 commits"

    x = hg.out('status -A')
    assert not x, "still no files should be reported by hg"
