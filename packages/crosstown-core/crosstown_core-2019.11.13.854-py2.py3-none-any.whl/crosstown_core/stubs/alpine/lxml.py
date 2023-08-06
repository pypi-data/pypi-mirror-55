from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="lxml",
    git_repo="https://github.com/lxml/lxml",
    plat_build_deps=C_BUILD_DEPS | {"libxslt-dev", "libxml2-dev"},
    plat_install_deps={"libxslt", "libxml2"},
    topics=["ser"],
)
