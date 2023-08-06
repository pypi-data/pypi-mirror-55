from crosstown_core.models import Stub, Dep
from crosstown_core.models.alpine import C_BUILD_DEPS, EDGE_TESTING

stub = Stub(
    pkg="h5py",
    git_repo="https://github.com/h5py/h5py",
    build_plat_deps=C_BUILD_DEPS | {Dep(pkg="hdf5-dev", repo=EDGE_TESTING)},
    install_plat_deps={Dep(pkg="hdf5", repo=EDGE_TESTING)},
    topics=["ds"],
)
