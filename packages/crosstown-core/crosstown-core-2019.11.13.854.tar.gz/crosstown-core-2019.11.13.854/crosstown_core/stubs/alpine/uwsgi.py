from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="uwsgi",
    git_repo="https://github.com/unbit/uwsgi",
    plat_build_deps=C_BUILD_DEPS | {"linux-headers"},
    topics=["web"],
)
