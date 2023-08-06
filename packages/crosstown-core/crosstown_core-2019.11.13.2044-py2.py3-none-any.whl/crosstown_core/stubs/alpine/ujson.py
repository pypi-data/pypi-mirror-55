from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="ujson",
    git_repo="https://github.com/esnme/ultrajson",
    build_plat_deps=C_BUILD_DEPS,
    topics=["ser"],
)
