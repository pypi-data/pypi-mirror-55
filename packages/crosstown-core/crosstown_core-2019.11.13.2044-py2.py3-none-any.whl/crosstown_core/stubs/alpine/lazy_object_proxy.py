from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = SourceStub(
    pkg="lazy-object-proxy",
    git_repo="https://github.com/ionelmc/python-lazy-object-proxy",
    build_plat_deps=C_BUILD_DEPS,
    topics=["utils"],
)
