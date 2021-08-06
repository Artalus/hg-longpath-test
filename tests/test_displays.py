from hgl import Hg

def test_log(unpack_repo: Hg) -> None:
    x = unpack_repo.out('log -T x')
    assert x == 'x'
    x = unpack_repo.out(f'status -A file.txt')
    assert x == 'C file.txt'
