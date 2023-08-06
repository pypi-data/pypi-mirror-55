from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="lazy-object-proxy",
    git_repo="https://github.com/ionelmc/python-lazy-object-proxy",
    builder_image_prefix="git-",
    plat_build_deps=C_BUILD_DEPS,
    topics=["utils"],
)
