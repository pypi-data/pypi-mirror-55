from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="numpy",
    git_repo="https://github.com/numpy/numpy",
    plat_build_deps=C_BUILD_DEPS | {"openblas-dev"},
    plat_install_deps={"openblas", "lapack"},
    topics=["ds"],
)
