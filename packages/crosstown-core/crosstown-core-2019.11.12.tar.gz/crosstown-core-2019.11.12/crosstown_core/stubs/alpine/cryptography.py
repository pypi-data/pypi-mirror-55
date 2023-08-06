from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="cryptography",
    git_repo="https://github.com/pyca/cryptography",
    git_tag_prefix="",
    builder_image_prefix="git-",
    plat_build_deps=C_BUILD_DEPS | {"openssl-dev", "libffi-dev"},
    plat_install_deps={"openssl"},
    py_build_deps={"cffi"},
    topics=["sec"],
)
