from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="numexpr",
    git_repo="https://github.com/pydata/numexpr",
    build_plat_deps=CPP_BUILD_DEPS | {"openblas-dev"},
    install_plat_deps=CPP_INSTALL_DEPS | {"openblas", "lapack"},
    build_py_deps={"numpy"},
    topics=["ds"],
)
