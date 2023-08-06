from django_frontera.contrib.utils.version import get_semver_version, get_version

VERSION = (0, 0, 2, 'alpha', 0)

__version__ = get_version(VERSION)

# Required for npm package for frontend
__semver__ = get_semver_version(VERSION)