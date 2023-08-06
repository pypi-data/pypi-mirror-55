from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = SourceStub(
    pkg="cryptography",
    git_repo="https://github.com/pyca/cryptography",
    git_tag_prefix="",
    plat_build_deps=C_BUILD_DEPS | {"openssl-dev", "libffi-dev"},
    plat_install_deps={"openssl"},
    py_build_deps={"cffi"},
    topics=["sec"],
)
