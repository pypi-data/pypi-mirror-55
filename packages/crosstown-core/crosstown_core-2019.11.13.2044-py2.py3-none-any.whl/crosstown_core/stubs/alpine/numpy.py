from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="numpy",
    git_repo="https://github.com/numpy/numpy",
    build_plat_deps=C_BUILD_DEPS | {"openblas-dev"},
    install_plat_deps={"openblas", "lapack"},
    topics=["free", "ds"],
)
