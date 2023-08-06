from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="gevent",
    git_repo="https://github.com/gevent/gevent",
    plat_build_deps=C_BUILD_DEPS,
    topics=["utils"],
)
