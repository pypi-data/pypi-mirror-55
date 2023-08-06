import re


def canonical_package_name(package_name: str) -> str:
    return re.sub(r"[.\-_]+", "-", package_name).lower()
