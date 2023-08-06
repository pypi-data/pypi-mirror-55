from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="multidict",
    git_repo="https://github.com/aio-libs/multidict",
    plat_build_deps=C_BUILD_DEPS,
    topics=["utils"],
)
