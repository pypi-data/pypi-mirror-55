import attr
import enum
import typing
import importlib
from packaging.version import Version
from crosstown_core.utils import canonical_package_name


DEP_TYPE = typing.Union[str, "Dep"]


class Platform(enum.Enum):
    ALPINE3_10 = "alpine-3.10"


class Topic(enum.Enum):
    DATA_SCIENCE = "ds"
    DATABASES = "db"
    SERIALIZATION = "ser"
    SECURITY = "sec"
    MACHINE_LEARNING = "ml"
    WEB_APPLICATIONS = "web"
    NATURAL_LANGUAGE_PROCESSING = "nlp"
    IMAGE_PROCESSING = "img"
    TRANSPORT = "tp"
    UTILITIES = "utils"
    GEOSPACIAL = "geo"


@attr.s(frozen=True, hash=True)
class Dep:
    pkg: str = attr.ib()
    pkg_ver: typing.Optional[str] = attr.ib(default=None)
    repo: typing.Optional[str] = attr.ib(default=None)

    @staticmethod
    def load(value: DEP_TYPE) -> "Dep":
        return value if isinstance(value, Dep) else Dep(pkg=value)


@attr.s
class BuildSpec:
    pkg: str = attr.ib()
    pkg_ver: typing.Optional[Version] = attr.ib()
    plat: Platform = attr.ib()
    py_ver: typing.Tuple[int, int] = attr.ib()

    def potential_stub_modules(self) -> typing.List[str]:
        pkg_mod = canonical_package_name(self.pkg).replace("-", "_")
        if self.plat == Platform.ALPINE3_10:
            return [
                f"crosstown_core.stubs.alpine_3_10.{pkg_mod}",
                f"crosstown_core.stubs.alpine.{pkg_mod}",
            ]
        raise ValueError()

    def get_stub(self) -> "Stub":
        for mod_name in self.potential_stub_modules():
            try:
                mod = importlib.import_module(mod_name)
                return mod.stub
            except (ImportError, AttributeError) as e:
                pass
        raise LookupError(f"cant find a stub for package {self.pkg}")


@attr.s
class Stub:
    pkg: str = attr.ib()
    git_repo: str = attr.ib()
    topics: typing.List[typing.Union[str, Topic]] = attr.ib(
        default=[], converter=lambda x: [Topic(i) for i in x]
    )
    git_tag_prefix: str = attr.ib(default="v")
    plat_build_deps: typing.Collection[DEP_TYPE] = attr.ib(default=[])
    plat_install_deps: typing.Collection[DEP_TYPE] = attr.ib(default=[])
    build_env_vars: typing.Dict[str, str] = attr.ib(default={})
    py_build_deps: typing.Collection[DEP_TYPE] = attr.ib(default=[])
    py_requires: typing.Optional[str] = attr.ib(default=None)
    builder_image_prefix: str = attr.ib(default="")
    builder_script_before_wheel = attr.ib(default=())
    pkg_import_name: str = attr.ib(default=None)

    def get_git_tag(self, spec: BuildSpec) -> str:
        return f"{self.git_tag_prefix}{spec.pkg_ver}"

    def get_plat_build_deps(self, spec: BuildSpec) -> typing.Collection[Dep]:
        return [Dep.load(x) for x in self.plat_build_deps or []]

    def get_plat_install_deps(self, spec: BuildSpec) -> typing.Collection[Dep]:
        return [Dep.load(x) for x in self.plat_install_deps or []]

    def get_py_build_deps(self, spec: BuildSpec) -> typing.Collection[Dep]:
        return [Dep.load(x) for x in self.py_build_deps or []]

    def get_builder_image_tag(self, spec: BuildSpec) -> str:
        return (
            f"{self.builder_image_prefix}python-{spec.py_ver[0]}.{spec.py_ver[1]}-{spec.plat.value}"
        )

    def get_pkg_import_name(self) -> str:
        return self.pkg_import_name or self.pkg.replace("-", "_")
