from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = SourceStub(
    pkg="bcrypt",
    git_repo="https://github.com/pyca/bcrypt",
    git_tag_prefix="",
    build_plat_deps=C_BUILD_DEPS | {"libffi-dev"},
    build_py_deps={"pycparser", "cffi", "setuptools"},
    topics=["sec"],
)
