from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="uvloop",
    git_repo="https://github.com/magicstack/uvloop",
    plat_build_deps=C_BUILD_DEPS,
    topics=["web", "utils"],
)
