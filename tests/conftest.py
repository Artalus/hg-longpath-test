import pytest
import tarfile

from hgl import Hg

# TODO: make customizable
REPO_TGZ = 'repo.tgz'

@pytest.fixture(scope='function')
def unpack_repo(tmpdir_factory: pytest.TempdirFactory) -> Hg:
    local = ("%s" % tmpdir_factory.mktemp("repo")).replace("\\", "/")
    with tarfile.open(REPO_TGZ, 'r:gz') as tar:
        tar.extractall(local)
    return Hg(workdir=local)
