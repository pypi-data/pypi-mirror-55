from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="cffi",
    git_repo="https://bitbucket.org/cffi/cffi",
    plat_build_deps=C_BUILD_DEPS | {"libffi-dev"},
    topics=["utils"],
)
