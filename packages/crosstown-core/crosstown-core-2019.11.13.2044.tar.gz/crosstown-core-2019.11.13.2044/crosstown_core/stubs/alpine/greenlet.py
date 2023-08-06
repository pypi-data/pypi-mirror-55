from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="greenlet",
    git_repo="https://github.com/python-greenlet/greenlet",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS,
    topics=["utils"],
)
