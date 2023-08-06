from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="thinc",
    git_repo="https://github.com/explosion/thinc",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS,
    py_build_deps=["cython", "cymem", "numpy", "preshed", "murmurhash", "blis"],
    topics=["nlp"],
)
