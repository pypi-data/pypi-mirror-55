from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="protobuf",
    git_repo="https://github.com/protocolbuffers/protobuf",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS,
    topics=["ser"],
)
