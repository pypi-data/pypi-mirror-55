from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="grpcio",
    git_repo="https://github.com/grpc/grpc",
    plat_build_deps=CPP_BUILD_DEPS | {"zlib-dev"},
    plat_install_deps=CPP_INSTALL_DEPS,
    topics=["ser"],
    pkg_import_name="grpc",
)
