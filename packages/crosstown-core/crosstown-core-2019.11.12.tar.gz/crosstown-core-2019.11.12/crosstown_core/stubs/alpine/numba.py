from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS

stub = Stub(
    pkg="numba",
    git_repo="https://github.com/numba/numba",
    plat_build_deps=CPP_BUILD_DEPS | {"llvm-dev", "openblas-dev"},
    plat_install_deps={"llvm8"},
    py_build_deps={"numpy"},
    topics=["ds"],
)
