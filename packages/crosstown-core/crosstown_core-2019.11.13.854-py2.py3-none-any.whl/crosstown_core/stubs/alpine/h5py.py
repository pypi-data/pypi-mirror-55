from crosstown_core.models import Stub, Dep
from crosstown_core.models.alpine import C_BUILD_DEPS, EDGE_TESTING

stub = Stub(
    pkg="h5py",
    git_repo="https://github.com/h5py/h5py",
    plat_build_deps=C_BUILD_DEPS | {Dep(pkg="hdf5-dev", repo=EDGE_TESTING)},
    plat_install_deps={Dep(pkg="hdf5", repo=EDGE_TESTING)},
    topics=["ds"],
    pkg_import_name="h5py",
)
