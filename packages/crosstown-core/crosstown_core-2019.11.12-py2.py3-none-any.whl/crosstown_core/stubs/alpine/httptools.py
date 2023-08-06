from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="httptools",
    git_repo="https://github.com/magicstack/httptools",
    plat_build_deps=C_BUILD_DEPS,
    topics=["web"],
)
