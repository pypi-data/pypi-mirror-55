from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = Stub(
    pkg="cchardet",
    git_repo="https://github.com/PyYoshi/cChardet",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS,
    topics=["nlp"],
)
