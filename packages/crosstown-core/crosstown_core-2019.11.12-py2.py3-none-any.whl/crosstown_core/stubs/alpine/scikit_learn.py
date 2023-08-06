from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="scikit-learn",
    git_repo="https://github.com/scikit-learn/scikit-learn",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS | {"openblas", "lapack"},
    py_build_deps={"numpy", "cython"},
    topics=["ds"],
)
