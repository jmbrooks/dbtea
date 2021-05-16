import platform
import sys

import dbt.semver as dbt_semver
import dbt.version as dbt_version

from dbtea import __version__
from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger


DBT_MIN_COMPATIBLE_VERSION = "0.17.0"


def check_installed_dbt_version() -> None:
    """"""
    logger.debug("dbt version details:\n{}".format(dbt_version.get_version_information()))
    logger.info("Running with dbt version: {}".format(dbt_version.get_installed_version()))
    if not _is_installed_dbt_version_compatible():
        raise DbteaException(
            name="unsupported-dbt-version",
            title="dbt version requires ",
            detail="You are currently using incompatible dbt version: {}".format(dbt_version.get_installed_version())
        )


def check_installed_python_version() -> None:
    """"""
    logger.debug("Running with Python version: {}".format(platform.version()))
    if sys.version_info < (3, 7):
        raise DbteaException(
            name="unsupported-python-version",
            title="dbtea requires Python 3.7 or higher",
            detail="You are currently using Python version: {}".format(platform.version())
        )


def get_dbtea_version_info() -> None:
    """"""
    logger.info("Running dbtea version: {}".format(dbt_semver.VersionSpecifier.from_version_string(__version__)))


def _is_installed_dbt_version_compatible() -> bool:
    """"""
    installed_dbt_version = dbt_version.get_installed_version()
    if installed_dbt_version < dbt_semver.VersionSpecifier.from_version_string(DBT_MIN_COMPATIBLE_VERSION):
        return False
    else:
        return True
