from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="gensim",
    git_repo="https://github.com/RaRe-Technologies/gensim",
    git_tag_prefix="",
    build_plat_deps=C_BUILD_DEPS | {"openblas-dev"},
    install_plat_deps={"openblas"},
    topics=["ds", "ml", "nlp"],
)
