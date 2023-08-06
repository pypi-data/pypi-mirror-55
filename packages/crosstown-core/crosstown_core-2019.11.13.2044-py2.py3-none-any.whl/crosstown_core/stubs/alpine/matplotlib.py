from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="matplotlib",
    git_repo="https://github.com/matplotlib/matplotlib",
    build_plat_deps=CPP_BUILD_DEPS | {"freetype-dev", "libpng-dev"},
    install_plat_deps=CPP_INSTALL_DEPS | {"freetype", "libpng"},
    topics=["ds"],
)
