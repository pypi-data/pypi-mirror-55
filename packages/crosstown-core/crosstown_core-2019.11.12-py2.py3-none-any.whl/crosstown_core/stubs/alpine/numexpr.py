from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="numexpr",
    git_repo="https://github.com/pydata/numexpr",
    plat_build_deps=CPP_BUILD_DEPS | {"openblas-dev"},
    plat_install_deps=CPP_INSTALL_DEPS | {"openblas", "lapack"},
    py_build_deps={"numpy"},
    topics=["ds"],
)
