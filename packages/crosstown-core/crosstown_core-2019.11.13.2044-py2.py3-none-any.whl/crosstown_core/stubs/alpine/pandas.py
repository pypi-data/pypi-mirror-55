from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="pandas",
    git_repo="https://github.com/pandas-dev/pandas",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS,
    build_py_deps={"numpy"},
    topics=["ds"],
)
