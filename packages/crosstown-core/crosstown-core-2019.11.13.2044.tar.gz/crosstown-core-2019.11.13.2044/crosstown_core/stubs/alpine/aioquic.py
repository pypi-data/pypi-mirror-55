from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="aioquic",
    git_repo="https://github.com/aiortc/aioquic",
    build_plat_deps=C_BUILD_DEPS | {"openssl-dev"},
    install_plat_deps={"openssl"},
    topics=["tp", "sec"],
)
