from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS

stub = Stub(
    pkg="numba",
    git_repo="https://github.com/numba/numba",
    build_plat_deps=CPP_BUILD_DEPS | {"llvm-dev", "openblas-dev"},
    install_plat_deps={"llvm8"},
    build_py_deps={"numpy"},
    topics=["ds"],
)
