import pathlib
import click
import typing
import sys
import subprocess
from packaging.version import Version
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
                    pkg_ver = None

                spec = BuildSpec(pkg=pkg, pkg_ver=pkg_ver, plat=plat, py_ver=py_ver)
                stub = spec.get_stub()

                docker_cmd = ["set -exo"]

                if stub.build_env_vars:
                    docker_cmd.append(
                        " ".join(f"export {k}={v}" for k, v in stub.build_env_vars.items())
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

                docker_cmd.extend(make_apk_installs(stub.get_plat_build_deps(spec)))
                docker_cmd.extend(make_apk_installs(stub.get_plat_install_deps(spec)))
                docker_cmd.extend(make_python_installs(stub.get_py_build_deps(spec)))
                docker_cmd.extend(stub.builder_script_before_wheel)
                docker_cmd.append("/bin/sh build-wheel.sh")

                builder_image = f"getcrosstown/builder:{stub.get_builder_image_tag(spec)}"
                cmd = (
                    f"docker run --rm -it "
                    f"-v {wheel_dir}:/wheels "
                    f"-e CROSSTOWN_PACKAGE_NAME={spec.pkg} "
                    f"-e CROSSTOWN_PACKAGE_VERSION={spec.pkg_ver if spec.pkg_ver else ''} "
                    f"-e CROSSTOWN_WHEEL_DIR=/wheels/{spec.plat.value} "
                    f'-e CROSSTOWN_GIT_REPO="{stub.git_repo}" '
                    f"-e CROSSTOWN_GIT_TAG={stub.get_git_tag(spec)} "
                    f"{builder_image} "
                    f"/bin/sh -c \"{'; '.join(docker_cmd)}\""
                )
                execute(cmd)

    if upload_wheels:
        execute(f"gsutil -m cp -n -r {wheel_dir}/* gs://pkgs-crosstown-dev-wheels/")
