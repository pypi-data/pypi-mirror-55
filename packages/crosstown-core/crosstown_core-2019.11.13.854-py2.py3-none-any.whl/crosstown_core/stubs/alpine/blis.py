from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="blis",
    git_repo="https://github.com/explosion/cython-blis",
    plat_build_deps=CPP_BUILD_DEPS | {"gfortran", "openblas-dev"},
    plat_install_deps=CPP_INSTALL_DEPS | {"openblas"},
    py_build_deps=["cython"],
    topics=["ds"],
)
