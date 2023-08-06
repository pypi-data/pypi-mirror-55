from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="aiohttp",
    git_repo="https://github.com/aio-libs/aiohttp",
    build_plat_deps=C_BUILD_DEPS,
    topics=["web"],
)
