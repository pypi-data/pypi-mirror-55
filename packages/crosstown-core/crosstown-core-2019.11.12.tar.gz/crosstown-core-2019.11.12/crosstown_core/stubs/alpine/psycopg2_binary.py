from crosstown_core.models import Stub
from crosstown_core.models.alpine import C_BUILD_DEPS

stub = Stub(
    pkg="psycopg2-binary",
    git_repo="https://github.com/psycopg/psycopg2",
    plat_build_deps=C_BUILD_DEPS | {"postgresql-dev"},
    plat_install_deps={"postgresql"},
    topics=["db"],
    pkg_import_name="psycopg2",
)
