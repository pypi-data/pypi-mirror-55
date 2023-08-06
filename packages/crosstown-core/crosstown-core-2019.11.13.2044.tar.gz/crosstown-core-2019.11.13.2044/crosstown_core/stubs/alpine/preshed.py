from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="preshed",
    git_repo="https://github.com/explosion/preshed",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS,
    build_py_deps=["cython", "cymem", "murmurhash"],
    topics=["utils"],
)
