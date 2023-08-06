from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="bjoern",
    git_repo="https://github.com/jonashaag/bjoern",
    plat_build_deps=C_BUILD_DEPS | {"libev-dev"},
    plat_install_deps={"libev"},
    topics=["web"],
)
