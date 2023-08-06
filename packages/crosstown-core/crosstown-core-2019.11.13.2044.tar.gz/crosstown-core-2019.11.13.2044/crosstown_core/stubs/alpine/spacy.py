from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import CPP_INSTALL_DEPS, CPP_BUILD_DEPS

stub = SourceStub(
    pkg="spacy",
    git_repo="https://github.com/explosion/spaCy",
    build_plat_deps=CPP_BUILD_DEPS,
    install_plat_deps=CPP_INSTALL_DEPS | {"openblas"},
    build_py_deps=["cython", "cymem", "thinc", "preshed"],
    topics=["nlp"],
)
