import pathlib
import click
import typing
import sys
import subprocess
import requests
from packaging.version import Version, InvalidVersion
from crosstown_core.models import BuildSpec, Platform


def execute(cmd) -> None:
    print(cmd)
    subprocess.check_call(cmd, shell=True, stdout=sys.stdout, stderr=subprocess.STDOUT)


@click.group()
def cli():
    pass


@cli.command()
@click.option("--python-versions", default="3.6,3.7,3.8")
@click.option("--platforms", default="alpine-3.10")
@click.option("--wheel-dir", default=pathlib.Path.home() / "wheels")
@click.option("--upload-wheels", is_flag=True)
@click.argument("pkgs", nargs=-1)
def wheel(
    python_versions: str,
    platforms: str,
    wheel_dir: pathlib.Path,
    upload_wheels: bool,
    pkgs: typing.Sequence[str],
):
    py_vers = python_versions.split(",")
    plats = platforms.split(",")

    pkg_latest: typing.Dict[str, str] = {}

    for py_ver in py_vers:
        py_ver = tuple([int(x) for x in py_ver.split(".")])
        assert len(py_ver) == 2
        for plat in plats:
            plat = Platform(plat)
            for pkg in pkgs:
                if "==" in pkg:
                    pkg, _, pkg_ver = pkg.partition("==")
                    pkg_ver = Version(pkg_ver)
                else:
                    if pkg not in pkg_latest:
                        resp = requests.get(f"https://pypi.org/pypi/{pkg}/json")
                        resp.raise_for_status()
                        pkgs_vers = []
                        for pypi_ver in resp.json()["releases"]:
                            try:
                                ver = Version(pypi_ver)
                            except InvalidVersion:
                                continue
                            if (
                                not ver.is_devrelease
                                and not ver.is_postrelease
                                and not ver.is_devrelease
                            ):
                                pkgs_vers.append(ver)
                        pkg_latest[pkg] = str(max(pkgs_vers))

                    pkg_ver = pkg_latest[pkg]

                spec = BuildSpec(pkg=pkg, pkg_ver=pkg_ver, plat=plat, py_ver=py_ver)
                stub = spec.get_stub()

                docker_cmd = ["set -exo"]
                docker_cmd.extend(
                    [f"export {k}={v}" for k, v in stub.get_build_env_vars(spec).items()]
                )

                def make_apk_installs(deps) -> typing.List[str]:
                    cmds = []
                    deps_no_repo = [dep for dep in deps if not dep.repo]
                    if deps_no_repo:
                        cmds.append(f"apk add {' '.join(dep.pkg for dep in deps_no_repo)}")
                    for dep in deps:
                        if dep.repo:
                            cmds.append(f"apk add {dep.pkg} --repository={dep.repo}")
                    return cmds

                def make_python_installs(deps) -> typing.List[str]:
                    if not deps:
                        return []
                    return [
                        "python -m pip install "
                        "--index-url=https://pkgs.crosstown.dev "
                        "--disable-pip-version-check "
                        f"{' '.join(dep.pkg for dep in deps)}"
                    ]

                docker_cmd.extend(make_apk_installs(stub.get_build_plat_deps(spec)))
                docker_cmd.extend(make_apk_installs(stub.get_install_plat_deps(spec)))
                docker_cmd.extend(make_python_installs(stub.get_build_py_deps(spec)))
                docker_cmd.extend(stub.get_build_script(spec))

                builder_image = f"getcrosstown/builder:{stub.get_builder_image_tag(spec)}"
                cmd = (
                    f"docker run --rm -it "
                    f"-v {wheel_dir / str(plat.value)}:/wheels "
                    f"{builder_image} "
                    f"/bin/sh -c \"{'; '.join(docker_cmd)}\""
                )
                execute(cmd)

    if upload_wheels:
        execute(f"gsutil -m cp -n -r {wheel_dir}/* gs://pkgs-crosstown-dev-wheels/")
