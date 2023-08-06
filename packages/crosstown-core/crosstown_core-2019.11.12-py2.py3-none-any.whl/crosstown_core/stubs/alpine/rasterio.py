from crosstown_core.models import Stub, Dep
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS, EDGE_TESTING

stub = Stub(
    pkg="rasterio",
    git_repo="https://github.com/mapbox/rasterio",
    git_tag_prefix="",
    builder_image_prefix="git-",
    plat_build_deps=CPP_BUILD_DEPS | {"openblas-dev", Dep("gdal-dev", repo=EDGE_TESTING)},
    plat_install_deps=CPP_INSTALL_DEPS
    | {Dep("gdal-dev", repo=EDGE_TESTING), Dep("proj", repo=EDGE_TESTING)},
    py_build_deps={"cython", "numpy"},
    topics=["geo"],
)
