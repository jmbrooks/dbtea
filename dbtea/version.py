import platform
import sys

from dbtea.exceptions import DbteaException

DBT_MIN_COMPATIBLE_VERSION = "0.17.0"


def check_installed_python_version() -> None:
    if sys.version_info < (3, 7):
        raise DbteaException(
            name="unsupported-python-version",
            title="dbtea requires Python 3.7 or higher",
            detail="You are currently using Python version {}".format(
                platform.version()
            ),
        )
