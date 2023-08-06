import typing
import pathlib
from crosstown_core.models import SourceStub, BuildSpec


class TorchStub(SourceStub):
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
            r"sed -ri 's/(Caffe2_DEPENDENCY_LIBS dl)/\1 execinfo/' CMakeLists.txt",
            (
                'sed -ri \'s/CMAKE_SHARED_LINKER_FLAGS \\"-Wl,--no-as-needed\\"/'
                'CMAKE_SHARED_LINKER_FLAGS \\"-Wl,--no-as-needed,-lexecinfo\\"/\' CMakeLists.txt'
            ),
            f"mkdir -p {wheel_dir}",
            "python setup.py bdist_wheel",
            f"cp dist/* {wheel_dir}",
        ]

    def get_build_env_vars(self, spec: BuildSpec) -> typing.Dict[str, str]:
        return {
            "USE_NUMPY": "1",
            "BLAS": "OpenBLAS",
            "EXTRA_CAFFE2_CMAKE_FLAGS": '"-DBLAS=OpenBLAS"',
            "PYTORCH_BUILD_VERSION": str(spec.pkg_ver),
            "PYTORCH_BUILD_NUMBER": "0",
        }


stub = TorchStub(
    pkg="torch",
    git_repo="https://github.com/pytorch/pytorch",
    build_plat_deps={"openblas-dev", "libexecinfo-dev", "linux-headers"},
    build_py_deps={"pyyaml", "numpy"},
    install_plat_deps={"openblas", "libexecinfo"},
    topics=["ml"],
)
