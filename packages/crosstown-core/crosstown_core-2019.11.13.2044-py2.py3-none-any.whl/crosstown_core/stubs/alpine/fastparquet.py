from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="fastparquet",
    git_repo="https://github.com/dask/fastparquet",
    git_tag_prefix="",
    build_plat_deps=C_BUILD_DEPS,
    topics=["ds"],
)
