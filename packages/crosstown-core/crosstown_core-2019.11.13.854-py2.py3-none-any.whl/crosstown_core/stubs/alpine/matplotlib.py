from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="matplotlib",
    git_repo="https://github.com/matplotlib/matplotlib",
    plat_build_deps=CPP_BUILD_DEPS | {"freetype-dev", "libpng-dev"},
    plat_install_deps=CPP_INSTALL_DEPS | {"freetype", "libpng"},
    topics=["ds"],
)
