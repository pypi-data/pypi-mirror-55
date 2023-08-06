import re
import pathlib
import datetime
import nox


base_dir: pathlib.Path = pathlib.Path(__file__).parent


@nox.session(reuse_venv=True)
def lint(session):
    session.install("--upgrade", "black")
    session.run(
        "black",
        "--target-version=py36",
        "--line-length=100",
        str(base_dir / "crosstown_core"),
        str(base_dir / "noxfile.py"),
    )

    check(session)


@nox.session(reuse_venv=True)
def check(session):
    session.install("--upgrade", "black", "flake8")
    session.run(
        "black",
        "--check",
        "--target-version=py36",
        "--line-length=100",
        str(base_dir / "crosstown_core"),
        str(base_dir / "noxfile.py"),
    )
    session.run(
        "flake8",
        "--max-line-length=100",
        str(base_dir / "crosstown_core"),
        str(base_dir / "noxfile.py"),
    )


@nox.session()
def build(session):
    session.install("flit")

    # Get the latest version of 'master'
    session.run("git", "checkout", "master", external=True)
    session.run("git", "pull", "origin", "master", external=True)

    # Replace the __version__ with the current day
    now = datetime.datetime.now()
    version = f"{now.year}.{now.month}.{now.day}.{now.hour}{str(now.minute).zfill(2)}"
    with (base_dir / "crosstown_core/__init__.py").open(mode="r") as f:
        data = f.read()
    data = re.sub(r"__version__\s+=\s+[\'\"][\d.]+[\'\"]", f'__version__ = "{version}"', data)
    with (base_dir / "crosstown_core/__init__.py").open(mode="w") as f:
        f.truncate()
        f.write(data)

    # Build wheels and tag the latest version in git
    session.run("git", "add", str(base_dir / "crosstown_core/__init__.py"), external=True)
    session.run("git", "commit", "-m", f"Release {version}", external=True)
    session.run("flit", "build")
    session.run("git", "tag", "-a", version, "-m", version, external=True)

    session.log("Built a release commit and dists, if this looks good run 'nox -s publish'")


@nox.session()
def publish(session: nox.sessions.Session):
    session.install("flit")
    session.run("flit", "publish")
    session.run("git", "push", "origin", "master", "--tags", external=True)
