from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="bcrypt",
    git_repo="https://github.com/pyca/bcrypt",
    git_tag_prefix="",
    builder_image_prefix="git-",
    plat_build_deps=C_BUILD_DEPS | {"libffi-dev"},
    py_build_deps={"pycparser", "cffi", "setuptools"},
    topics=["sec"],
)
