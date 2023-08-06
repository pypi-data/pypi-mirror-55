from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="cymem",
    git_repo="https://github.com/explosion/cymem",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS,
    py_build_deps=["cython"],
    topics=["utils"],
)
