from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="scipy",
    git_repo="https://github.com/scipy/scipy",
    build_plat_deps=CPP_BUILD_DEPS | {"openblas-dev"},
    install_plat_deps=CPP_INSTALL_DEPS | {"openblas", "lapack"},
    build_py_deps=["numpy", "cython"],
    topics=["ds"],
)
