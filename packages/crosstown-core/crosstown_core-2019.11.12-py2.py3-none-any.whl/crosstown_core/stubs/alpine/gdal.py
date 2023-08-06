from crosstown_core.models import Stub, Dep
from crosstown_core.models.alpine import CPP_BUILD_DEPS, CPP_INSTALL_DEPS, EDGE_TESTING

# Currently Alpine only supports GDAL 2.X
# despite 3.X being released for a few months
stub = Stub(
    pkg="gdal",
    git_repo="https://github.com/OSGeo/gdal",
    plat_build_deps=CPP_BUILD_DEPS | {"openblas-dev", Dep("gdal-dev", repo=EDGE_TESTING)},
    plat_install_deps=CPP_INSTALL_DEPS | {Dep("gdal", repo=EDGE_TESTING)},
    py_build_deps={"numpy"},
    topics=["geo"],
)
