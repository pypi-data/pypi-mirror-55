import typing
import pathlib
from crosstown_core.models import SourceStub, BuildSpec, Dep
from crosstown_core.models.alpine import EDGE_TESTING


class TensorflowStub(SourceStub):
    def get_build_script(self, spec: BuildSpec) -> typing.List[str]:
        wheel_dir = str(pathlib.Path("/wheels") / spec.pkg)
        return [
            "mkdir /repo",
            (
                f"git clone -b {self.get_git_tag(spec)} "
                f"--single-branch "
                f"--recurse-submodules -j4 "
                f"{self.git_repo} /repo"
            ),
            "cd /repo",
            f"mkdir -p {wheel_dir}",
            f"patch -p1 < ../tensorflow-{spec.pkg_ver}.patch",
            "bash configure",
            (
                "bazel build -c opt --verbose_failures "
                "//tensorflow/tools/pip_package:build_pip_package"
            ),
            "bazel-bin/tensorflow/tools/pip_package/build_pip_package ./dist",
            f"cp dist/* {wheel_dir}",
        ]


stub = TensorflowStub(
    pkg="tensorflow",
    git_repo="https://github.com/tensorflow/tensorflow",
    build_plat_deps={
        "libc6-compat",
        "libexecinfo-dev",
        "libunwind-dev",
        "bash",
        "build-base",
        "patch",
        "perl",
        "sed",
        Dep("hdf5-dev", repo=EDGE_TESTING),
    },
    build_py_deps={"numpy", "h5py", "keras-applications", "keras-preprocessing"},
    install_plat_deps={},
    topics=["ml"],
)
