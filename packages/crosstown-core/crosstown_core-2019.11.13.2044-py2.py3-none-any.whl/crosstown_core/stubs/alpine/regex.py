from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="regex",
    git_repo="https://bitbucket.org/mrabarnett/mrab-regex",
    build_plat_deps=C_BUILD_DEPS,
    topics=["utils"],
)
