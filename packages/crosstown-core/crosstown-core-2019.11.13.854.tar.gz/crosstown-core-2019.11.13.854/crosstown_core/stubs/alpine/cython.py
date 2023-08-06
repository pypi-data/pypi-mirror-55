from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="cython",
    git_repo="https://github.com/cython/cython",
    plat_build_deps=C_BUILD_DEPS,
    topics=["free", "utils"],
)
