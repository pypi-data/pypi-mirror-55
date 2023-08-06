from crosstown_core.models import Stub
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS

stub = Stub(
    pkg="msgpack-python",
    git_repo="https://github.com/msgpack/msgpack-python",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS,
    build_py_deps={"cython"},
    topics=["ser"],
)
