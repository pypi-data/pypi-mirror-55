import typing
import attr
import pathlib
import subprocess
import errno
import shutil
import glob


base_dir: pathlib.Path = pathlib.Path(__file__).parent
base_images_dir: pathlib.Path = base_dir / "images"


@attr.s
class Instruction:
    command: str = attr.ib()
    content: str = attr.ib()

    def render(self) -> str:
        return f"{self.command} {self.content}"


class Image:
    def __init__(self, image_name: str, image_dir: pathlib.Path):
        self.image_name = image_name
        self.image_dir = image_dir
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.instructions: typing.List[Instruction] = []

    def from_image(self, image: str, image_name: str = None):
        self.instructions.append(Instruction("FROM", f"{image}{'' if image_name is None else ' AS ' + image_name}"))

    def env(self, name, value):
        self.instructions.append(Instruction("ENV", f"{name} {value}"))

    def run(self, *argv):
        self.instructions.append(Instruction("RUN", " && \\\n    ".join(argv).rstrip()))

    def copy(self, src: typing.Union[str, typing.Sequence[str]], dest: str, *, from_image: str=None):
        if isinstance(src, str):
            src = (src,)
        args = tuple(src) + (dest,)
        if from_image is not None:
            args = (f"--from={from_image}",) + args
        self.instructions.append(Instruction("COPY", " ".join(args)))

    def workdir(self, dir: str):
        self.instructions.append(Instruction("WORKDIR", dir))

    def build(self, force: bool=False):
        dockerfile_data = "\n".join(["# This Dockerfile is auto-generated, don't edit manually!"] + [inst.render() for inst in self.instructions] + [""])
        dockerfile = self.image_dir / "Dockerfile"
        try:
            with dockerfile.open(mode="r") as f:
                data = f.read()
        except OSError as e:
            if e.errno == errno.ENOENT:
                data = ""
            else:
                raise

        if force or data != dockerfile_data:
            with dockerfile.open(mode="w") as f:
                f.truncate()
                f.write(dockerfile_data)

            subprocess.check_call(
                f"docker build {self.image_dir} "
                f"--tag {self.image_name}",
                shell=True
            )


def main():
    # Get this value from tensorflow/configure.py:_TF_MIN/MAX_BAZEL_VERSION
    bazel_version = "0.26.1"

    # Bazel
    for alpine_version in ["3.10"]:
        image = Image(
            image_name=f"getcrosstown/builder:bazel{bazel_version}-alpine-{alpine_version}",
            image_dir=base_images_dir / f"alpine-{alpine_version}" / f"bazel{bazel_version}"
        )
        image.from_image(f"alpine:{alpine_version}")
        image.env("BAZEL_VERSION", bazel_version)
        image.env("JAVA_HOME", "/usr/lib/jvm/default-jvm")

        image.run(
            "mkdir /tmp/bazel",
            "cd /tmp/bazel",
            "apk update",
            "apk add --no-cache bash openjdk8 libarchive wget zip git \\"
            "unzip coreutils git linux-headers protobuf python3 gcc g++",
            "ln /usr/bin/python3 /usr/bin/python",
            f"wget -q https://github.com/bazelbuild/bazel/releases/download/$BAZEL_VERSION/bazel-$BAZEL_VERSION-dist.zip",
            "unzip bazel-$BAZEL_VERSION-dist.zip",
            "rm bazel-$BAZEL_VERSION-dist.zip",
            "EXTRA_BAZEL_ARGS=--host_javabase=@local_jdk//:jdk ./compile.sh",
            "output/bazel shutdown",
            "echo startup --server_javabase=$JAVA_HOME >> scripts/packages/bazel.bazelrc",
            "install -Dm755 scripts/packages/bazel.sh /usr/bin/bazel",
            "install -Dm755 scripts/packages/bazel.bazelrc /etc/bazel.bazelrc",
            "install -Dm755 output/bazel /usr/bin/bazel-real",
            "cd /",
            "rm -rf /tmp/bazel"
        )
        image.build()

    # Python
    for python_version in ["3.8", "3.7", "3.6"]:
        for alpine_version in ["3.10"]:
            image = Image(
                image_name=f"getcrosstown/builder:python-{python_version}-alpine-{alpine_version}",
                image_dir=base_images_dir / f"alpine-{alpine_version}" / f"python-{python_version}"
            )
            image.from_image(f"python:{python_version}-alpine{alpine_version}")
            image.env("PYTHON_VERSION", python_version)
            image.env("JAVA_HOME", "/usr/lib/jvm/default-jvm")

            # Install Bazel
            bazel_image_name = f"getcrosstown/builder:bazel{bazel_version}-alpine-{alpine_version}"
            image.copy(src=("/usr/bin/bazel", "/usr/bin/bazel-real"), dest="/usr/bin/", from_image=bazel_image_name)
            image.copy("/etc/bazel.bazelrc", "/etc/", from_image=bazel_image_name)

            image.run(
                "apk update",
                "apk add --no-cache gcc g++ musl-dev python3-dev make cmake git"
            )
            image.build()

    # Tensorflow (Doesn't build on Python 3.8 yet!)
    for python_version in ["3.7", "3.6"]:
        for alpine_version in ["3.10"]:
            image = Image(
                image_name=f"getcrosstown/builder:tensorflow-python-{python_version}-alpine-{alpine_version}",
                image_dir=base_images_dir / f"alpine-{alpine_version}" / f"tensorflow-python-{python_version}"
            )
            image.from_image(f"getcrosstown/builder:python-{python_version}-alpine-{alpine_version}")

            image.run(
                "apk add --no-cache libc6-compat libexecinfo-dev libunwind-dev bash build-base patch perl sed",
                "apk add --no-cache hdf5-dev --repository=http://dl-3.alpinelinux.org/alpine/edge/testing",
                "python -m pip install --no-cache-dir --index-url=https://pkgs.crosstown.dev --extra-index-url=https://pypi.org/simple numpy h5py",
                "git clone https://github.com/tensorflow/tensorflow /tensorflow",
                "cd /tensorflow",
                "git submodule update --init --recursive",
            )
            image.workdir("/tensorflow")

            for patch_file in glob.glob(str(base_images_dir / "alpine-3.10/scripts/tensorflow/*.patch")):
                shutil.copy(patch_file, str(image.image_dir))
            shutil.copy(str(base_images_dir / "alpine-3.10/scripts/tensorflow/build-wheel.sh"), str(image.image_dir))
            image.copy("build-wheel.sh *.patch", "/tensorflow/")

            image.build()


if __name__ == "__main__":
    main()
