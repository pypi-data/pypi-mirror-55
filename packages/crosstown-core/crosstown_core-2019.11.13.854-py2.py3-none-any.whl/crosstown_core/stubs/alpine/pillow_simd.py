from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pillow-simd",
    git_repo="https://github.com/uploadcare/pillow-simd",
    plat_build_deps=C_BUILD_DEPS | {"libjpeg-turbo-dev", "libpng"},
    plat_install_deps={"libjpeg-turbo", "libpng"},
    build_env_vars={"CFLAGS": "-mavx2"},
    topics=["img"],
    pkg_import_name="PIL",
)
