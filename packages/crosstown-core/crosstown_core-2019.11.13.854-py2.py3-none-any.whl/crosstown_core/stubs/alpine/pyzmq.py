from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pyzmq",
    git_repo="https://github.com/zeromq/pyzmq",
    plat_build_deps=C_BUILD_DEPS | {"zeromq-dev"},
    plat_install_deps={"libzmq"},
    topics=["tp"],
)
