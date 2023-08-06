import typing
from crosstown_core.models import SourceStub, BuildSpec
from crosstown_core.models.alpine import C_BUILD_DEPS


class JaprontoSourceStub(SourceStub):
    """Japronto doesn't publish source wheels or consistent tags.
    Luckily they don't publish very often so this should
    be pretty easy to keep up with.
    """

    def get_build_script(self, spec: BuildSpec) -> typing.Sequence[str]:
        version_to_commit = {"0.1.2": "c6ed1c342b36dd4ddcbe22cd40b0ac03597229e2"}
        if str(spec.pkg_ver) not in version_to_commit:
            raise RuntimeError(f"Could not find commit for version {spec.pkg_ver}")

        commands = super().get_build_script(spec)
        for i in range(len(commands)):
            if "git clone" in commands[i] and self.get_git_tag(spec) in commands[i]:
                commands[i] = commands[i].replace(
                    self.get_git_tag(spec), version_to_commit[str(spec.pkg_ver)]
                )
                break

        return commands


stub = JaprontoSourceStub(
    pkg="japronto",
    git_repo="https://github.com/squeaky-pl/japronto",
    build_plat_deps=C_BUILD_DEPS,
    topics=["web"],
)
