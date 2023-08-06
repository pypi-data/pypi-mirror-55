from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="spacy",
    git_repo="https://github.com/explosion/spaCy",
    plat_build_deps=CPP_BUILD_DEPS,
    plat_install_deps=CPP_INSTALL_DEPS | {"openblas"},
    py_build_deps=["cython", "cymem", "thinc", "preshed"],
    topics=["nlp"],
)
