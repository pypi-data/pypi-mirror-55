from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="pillow",
    git_repo="https://github.com/python-pillow/pillow",
    build_plat_deps=C_BUILD_DEPS | {"libjpeg-turbo-dev", "libpng"},
    install_plat_deps={"libjpeg-turbo", "libpng"},
    topics=["free", "img"],
    module_import_name="PIL",
)
