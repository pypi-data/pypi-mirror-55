from crosstown_core.models import SourceStub, Dep
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS, EDGE_TESTING

stub = SourceStub(
    pkg="rasterio",
    git_repo="https://github.com/mapbox/rasterio",
    git_tag_prefix="",
    build_plat_deps=CPP_BUILD_DEPS | {"openblas-dev", Dep("gdal-dev", repo=EDGE_TESTING)},
    install_plat_deps=CPP_INSTALL_DEPS
    | {Dep("gdal-dev", repo=EDGE_TESTING), Dep("proj", repo=EDGE_TESTING)},
    build_py_deps={"cython", "numpy"},
    topics=["geo"],
)
