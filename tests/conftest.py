import tarfile

import pytest

from hgl import Hg

# TODO: make customizable
REPO_TAR = 'repo.tar'

@pytest.fixture(scope='function')
def unpack_repo(tmpdir_factory: pytest.TempdirFactory) -> Hg:
    local = ("%s" % tmpdir_factory.mktemp("repo")).replace("\\", "/")
    with tarfile.open(REPO_TAR, 'r') as tar:
        tar.extractall(local)
    return Hg(workdir=local)
