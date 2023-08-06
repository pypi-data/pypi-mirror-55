from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="astropy",
    git_repo="https://github.com/astropy/astropy",
    plat_build_deps=C_BUILD_DEPS,
    py_build_deps=["cython", "jinja2"],
    topics=["ds"],
)
