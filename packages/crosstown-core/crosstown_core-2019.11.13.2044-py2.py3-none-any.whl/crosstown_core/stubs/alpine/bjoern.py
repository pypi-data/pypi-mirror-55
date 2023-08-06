from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="bjoern",
    git_repo="https://github.com/jonashaag/bjoern",
    build_plat_deps=C_BUILD_DEPS | {"libev-dev"},
    install_plat_deps={"libev"},
    topics=["web"],
)
