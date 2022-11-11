from dataclasses import dataclass
from packaging.version import Version

@dataclass
class VersionFilter:
    odd_minor_development: bool = False

def is_odd_minor_development(version: Version) -> bool:
    return version.minor % 2 == 1

