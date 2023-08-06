from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pymongo",
    git_repo="https://github.com/mongodb/mongo-python-driver",
    build_plat_deps=C_BUILD_DEPS,
    topics=["db"],
)
