from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = SourceStub(
    pkg="bcrypt",
    git_repo="https://github.com/pyca/bcrypt",
    git_tag_prefix="",
    plat_build_deps=C_BUILD_DEPS | {"libffi-dev"},
    py_build_deps={"pycparser", "cffi", "setuptools"},
    topics=["sec"],
)
