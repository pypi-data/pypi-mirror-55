from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pylsqpack",
    git_repo="https://github.com/aiortc/pylsqpack",
    build_plat_deps=C_BUILD_DEPS,
    install_plat_deps={"bsd-compat-headers"},
    topics=["tp"],
)
