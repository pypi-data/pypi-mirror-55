from crosstown_core.models import SourceStub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = SourceStub(
    pkg="cryptography",
    git_repo="https://github.com/pyca/cryptography",
    git_tag_prefix="",
    build_plat_deps=C_BUILD_DEPS | {"openssl-dev", "libffi-dev"},
    install_plat_deps={"openssl"},
    build_py_deps={"cffi"},
    topics=["sec"],
)
