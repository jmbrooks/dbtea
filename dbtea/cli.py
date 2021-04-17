import argparse
import logging
import os
import sys
from typing import Callable

import dbtea.utils as utils
from dbtea.config import DbteaConfig, PROFILES_DIR
from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger
from dbtea.version import check_installed_python_version

# from dbtea import __version__


class EnvVarAction(argparse.Action):
    """Uses an argument default defined in an environment variable.
    Args:
        env_var: The name of the environment variable to get the default from.
        required: The argument's requirement status as defined in add_argument.
        default: The argument default as defined in add_argument.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(self, env_var, required=False, default=None, **kwargs):
        self.env_var = env_var
        if env_var in os.environ:
            default = os.environ[env_var]
        if required and default:
            required = False
        super().__init__(default=default, required=required, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Sets the argument value to the namespace during parsing.
        Args:
            parser: Parent argparse parser that is calling the action.
            namespace: Object where parsed values will be set.
            values: Parsed values to be set to the namespace.
            option_string: Argument string, e.g. "--optional".
        """
        setattr(namespace, self.dest, values)


def _build_base_subparser() -> argparse.ArgumentParser:
    """Returns the base subparser with arguments required for every subparser.
    Returns:
        argparse.ArgumentParser: Base subparser with url and auth arguments.
    """
    base_subparser = argparse.ArgumentParser(add_help=False)
    base_subparser.add_argument(
        "--profiles-dir",
        type=str,
        default=PROFILES_DIR,
        help="The directory to look for the profiles.yml file. Default: {}".format(
            PROFILES_DIR
        ),
    )
    base_subparser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        dest="log_level",
        const=logging.DEBUG,
        default=logging.INFO,
        help="Display debug logging during Spectacles execution. \
            Useful for debugging and making bug reports.",
    )
    base_subparser.add_argument(
        "--log-dir",
        action=EnvVarAction,
        env_var="DBTEA_LOG_DIR",
        default="logs",
        help="The directory that dbtea will write logs to.",
    )

    return base_subparser


def handle_exceptions(function: Callable) -> Callable:
    """Wrapper for handling custom exceptions by logging them.
    Args:
        function: Callable to wrap and handle exceptions for.
    Returns:
        callable: Wrapped callable.
    """

    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except DbteaException as error:
            logger.error(
                f"\n{error}\n\n"
                + "For support, please create an issue at https://github.com/spectacles-ci/spectacles/issues"
                + "\n"
            )
            sys.exit(error.exit_code)
        except KeyboardInterrupt as error:
            logger.debug(error, exc_info=True)
            logger.info("Spectacles was manually interrupted.")
            sys.exit(1)
        except Exception as error:
            logger.debug(error, exc_info=True)
            logger.error(
                f'\nEncountered unexpected {error.__class__.__name__}: "{error}"\n'
                f"Full error traceback logged to file.\n\n"
                + "For support, please create an issue at https://github.com/spectacles-ci/spectacles/issues"
                + "\n"
            )
            sys.exit(1)

    return wrapper


def create_parser() -> argparse.ArgumentParser:
    """Creates the top-level argument parser.

    Returns:
        argparse.ArgumentParser: Top-level argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="dbtea", description="Manage and administer dbt"
    )
    parser.add_argument(
        "--version", action="version", version="0.1.0", help="Current dbtea version"
    )
    # subparser_action = parser.add_subparsers(
    #     title="Available sub-commands", dest="command"
    # )
    #
    # base_subparser = _build_base_subparser()

    return parser


def main():
    """Execute dbtea, the primary entrypoint."""
    check_installed_python_version()

    parser = create_parser()
    args = parser.parse_args()
    print(args)

    # sample_path = "/tests/resources/dbt_projects/dim_date"
    # dbt_project_directory = utils.fetch_dbt_project_directory(sample_path)
    # dim_date_yaml = utils.parse_yaml_file(
    #     utils.assemble_path(dbt_project_directory, "models/marts/_core.yml")
    # )
    # print(dim_date_yaml)


if __name__ == "__main__":
    main()
