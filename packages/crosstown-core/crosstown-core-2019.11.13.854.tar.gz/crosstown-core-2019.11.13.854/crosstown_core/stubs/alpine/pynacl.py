from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pynacl",
    git_repo="https://github.com/pyca/pynacl",
    git_tag_prefix="",
    builder_image_prefix="git-",
    plat_build_deps=C_BUILD_DEPS | {"libsodium-dev", "libffi-dev"},
    plat_install_deps={"libsodium"},
    py_build_deps={"cffi"},
    topics=["sec"],
)
