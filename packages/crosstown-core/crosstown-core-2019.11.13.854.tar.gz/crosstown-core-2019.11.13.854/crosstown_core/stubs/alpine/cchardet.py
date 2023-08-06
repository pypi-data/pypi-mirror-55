from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = Stub(
    pkg="cchardet",
    git_repo="https://github.com/PyYoshi/cChardet",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS,
    topics=["nlp"],
)
