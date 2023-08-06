from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="pandas",
    git_repo="https://github.com/pandas-dev/pandas",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS,
    py_build_deps={"numpy"},
    topics=["ds"],
)
