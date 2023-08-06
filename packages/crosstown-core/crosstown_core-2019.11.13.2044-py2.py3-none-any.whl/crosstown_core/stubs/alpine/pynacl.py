from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pynacl",
    git_repo="https://github.com/pyca/pynacl",
    git_tag_prefix="",
    builder_image_prefix="git-",
    build_plat_deps=C_BUILD_DEPS | {"libsodium-dev", "libffi-dev"},
    install_plat_deps={"libsodium"},
    build_py_deps={"cffi"},
    topics=["sec"],
)
