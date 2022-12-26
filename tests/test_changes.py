from typing import Callable
import os

from pytest import mark

from hgl import Hg
from hgl.init import Const
from hgl.utils import windows, filepath, possible_hg_commands


HgTest = Callable[..., None]
def multiple_hg(func: HgTest) -> HgTest:
    return mark.parametrize("hg_cmd", possible_hg_commands())(func)


@multiple_hg
def test_add(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME_2)
    hg.write_file(fname)
    if windows() and hg.is_exe():
        rc = hg.code(f'add {fname}')
        assert rc, 'windows cannot add long paths'
    else:
        hg.do(f'add {fname}')
        x = hg.out(f'status -A {fname}').replace('\\', '/')
        assert x == f'A {fname}', 'long file should be marked for addition'


@multiple_hg
def test_rm(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    def long_file_exists() -> bool:
        with hg.chdir():
            return os.path.isfile(fname)

    # surprisingly, `hg rm` thinks file already deleted, does not touch filesystem, and actually marks it in hg
    assert long_file_exists(), "file exists before rm (of course)"

    x = hg.out(f'status -A {fname}').replace('\\', '/')
    if windows() and hg.is_exe():
        assert x == f'! {fname}', 'windows does not see long path and considers it deleted'
    else:
        assert x == f'C {fname}', 'long file should be safely committed'

    x = hg.out(f'rm {fname}')
    assert not x, "should success or do nothing"

    if windows() and hg.is_exe():
        assert long_file_exists(), "file should still exist after failed rm"
    else:
        assert not long_file_exists(), "file removed after rm"
    x = hg.out(f'status -A {fname}').replace('\\', '/')
    assert x == f'R {fname}', 'long file should be marked for removal'


@multiple_hg
def test_commit_adds(unpack_repo: str, hg_cmd: list[str]) -> None:
    # TODO: should be skipped if test_add fails, otherwise can report nonsence
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME_2)
    hg.write_file(fname)

    if windows() and hg.is_exe():
        rc = hg.code(f'add {fname}')
        assert rc, 'windows cannot add long path'

        before = hg.out('log -T "{node}"')
        rc = hg.commit_code('another long path')
        assert rc, 'windows cannot commit addition of long path'

        after = hg.out('log -T "{node}"')
        assert before == after, 'should still contain same commits'
    else:
        hg.do(f'add {fname}')
        hg.commit('another long path')
        x = hg.out('log -T x')
        assert x == 'xxx', 'should contain 3 commits'
        x = hg.out('status')
        assert not x, 'should not have changes to files'


@multiple_hg
def test_commit_removes(unpack_repo: str, hg_cmd: list[str]) -> None:
    # TODO: should be skipped if test_rm fails, otherwise can report nonsence
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    def long_file_exists() -> bool:
        with hg.chdir():
            return os.path.isfile(fname)

    assert long_file_exists(), "file exists before rm (of course)"
    # does not fail, see test_rm
    x = hg.out(f'rm {fname}')
    assert not x, "should success or do nothing"

    if windows() and hg.is_exe():
        assert long_file_exists(), "file should still exist after failed rm"

        hg.commit('remove long path')
        assert long_file_exists(), "file should still exist after failed commit"
    else:
        assert not long_file_exists(), "file removed after rm"

        hg.commit('remove long path')
        assert not long_file_exists(), "file stays removed after commit"

    x = hg.out(f'status -A {fname}')
    assert not x, "hg does not detect removed file"
    x = hg.out('log -T x')
    assert x == 'xxx', 'should contain 3 commits'
    x = hg.out('status')
    assert not x, 'should not have changes to tracked files'


@multiple_hg
def test_commit_changes(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    hg.write_file(fname, 'world hello')
    if windows() and hg.is_exe():
        before = hg.out('log -T "{node}"')
        rc = hg.commit_code('changed long path')
        assert rc, 'windows cannot commit changes in long paths'
        after = hg.out('log -T "{node}"')
        assert before == after, 'should still contain same commits'
    else:
        hg.commit('changed long path')
        x = hg.out('log -T x')
        assert x == 'xxx', 'should contain 3 commits'


@multiple_hg
def test_strip(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    def long_file_exists() -> bool:
        with hg.chdir():
            return os.path.isfile(filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME))

    if windows() and hg.is_exe():
        before = hg.out('log -T "{node}"')
        assert long_file_exists(), "file exists before strip (of course)"

        rc = hg.code('--config extensions.strip= strip -r .')
        assert rc, 'windows cannot remove long paths during strip'

        assert long_file_exists(), "file should still exist after failed strip"
        after = hg.out('log -T "{node}"')
        assert before == after, 'should still contain same commits'
    else:
        assert long_file_exists(), "file exists before strip (of course)"
        hg.do('--config extensions.strip= strip -r .')
        x = hg.out('log -T x')
        assert x == 'x', 'should contain 1 commit'
        assert not long_file_exists(), "file removed after strip"


@multiple_hg
def test_move(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    src = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    dst = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME_2)

    if windows() and hg.is_exe():
        rc = hg.code(f'mv {src} {dst}')
        assert rc, 'windows cannot move long file'
        with hg.chdir():
            assert os.path.isfile(src), "source file should remain"
            assert not os.path.isfile(dst), "destination file should not be"
        x = hg.out('status').splitlines()
        assert len(x) < 2, 'hg should not know about move, but can think file was deleted'
    else:
        hg.do(f'mv {src} {dst}')
        with hg.chdir():
            assert not os.path.isfile(src), "source file should be removed"
            assert os.path.isfile(dst), "destination file should be created"
        x = hg.out('status').splitlines()
        assert len(x) == 2, 'hg should know about move'


@multiple_hg
def test_update(unpack_repo: str, hg_cmd: list[str]) -> None:
    hg = Hg(workdir=unpack_repo, hg_cmd=hg_cmd)
    fname = filepath(Const.LONG_FOLDER_TREE, Const.LONG_FILE_NAME)
    def long_file_exists() -> bool:
        with hg.chdir():
            return os.path.isfile(fname)

    assert long_file_exists(), "file exists before update (of course)"
    hg.up('.^')
    if windows():
        # apparently, even using script instead of exe does not help in this case
        assert long_file_exists(), "on windows update does not remove file"
    else:
        assert not long_file_exists(), "file no longer exists after update to previous commit"
    hg.up()
    assert long_file_exists(), "file exists before update back"
