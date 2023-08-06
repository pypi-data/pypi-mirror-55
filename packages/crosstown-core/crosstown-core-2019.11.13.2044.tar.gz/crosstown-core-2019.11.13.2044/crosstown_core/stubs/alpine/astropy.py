from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="astropy",
    git_repo="https://github.com/astropy/astropy",
    build_plat_deps=C_BUILD_DEPS,
    build_py_deps=["cython", "jinja2"],
    topics=["ds"],
)
