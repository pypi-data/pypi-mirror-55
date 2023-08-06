from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="gensim",
    git_repo="https://github.com/RaRe-Technologies/gensim",
    git_tag_prefix="",
    plat_build_deps=C_BUILD_DEPS | {"openblas-dev"},
    plat_install_deps={"openblas"},
    topics=["ds", "ml", "nlp"],
)
