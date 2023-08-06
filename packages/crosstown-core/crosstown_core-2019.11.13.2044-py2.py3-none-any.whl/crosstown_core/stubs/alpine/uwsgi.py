from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="uwsgi",
    git_repo="https://github.com/unbit/uwsgi",
    build_plat_deps=C_BUILD_DEPS | {"linux-headers"},
    topics=["web"],
)
