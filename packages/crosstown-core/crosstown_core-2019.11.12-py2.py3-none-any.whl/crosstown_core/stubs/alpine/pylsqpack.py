from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pylsqpack",
    git_repo="https://github.com/aiortc/pylsqpack",
    plat_build_deps=C_BUILD_DEPS,
    plat_install_deps={"bsd-compat-headers"},
    topics=["tp"],
)
