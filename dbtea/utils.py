import functools
import json
import os
import subprocess
import timeit
from pathlib import Path
from typing import Callable, List, Union

import yaml

from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger

DBT_PROJECT_FILE = "dbt_project.yml"


def assemble_path(*args):
    """"""
    return os.path.join(*args)


def file_exists(file_path: str) -> bool:
    """"""
    return Path(file_path).is_file()


def fetch_dbt_project_directory(custom_project_directory: str = None) -> str:
    """Return path to the base of the closest dbt project by traversing from current working directory backwards in
    order to find a dbt_project.yml file.

    If an optional custom project path is specified (which should be a full path to the base project path of a dbt
    project), return that directory instead.
    """
    project_directory = os.getcwd()
    root_path = os.path.abspath(os.sep)

    if custom_project_directory:
        custom_directory_project_file = assemble_path(
            custom_project_directory, DBT_PROJECT_FILE
        )
        if os.path.exists(custom_directory_project_file):
            return custom_project_directory
        else:
            raise DbteaException(
                name="invalid-custom-dbt-project-directory",
                title="No dbt project found at supplied custom directory",
                detail="No dbt_project.yml file found at supplied custom project directory {}, confirm your "
                "custom project directory is valid".format(custom_project_directory),
            )

    while project_directory != root_path:
        dbt_project_file = assemble_path(project_directory, DBT_PROJECT_FILE)
        if os.path.exists(dbt_project_file):
            logger.info(
                "Running dbtea against dbt project at path: {}".format(
                    project_directory
                )
            )
            return project_directory

        project_directory = os.path.dirname(project_directory)

    raise DbteaException(
        name="missing-dbt-project",
        title="No dbt project found",
        detail="No dbt_project.yml file found in current or any direct parent paths. You need to run dbtea "
        "from within dbt project in order to use its tooling, or supply a custom project directory",
    )


def flatten_json(json_data: dict, delimiter: str = "_"):
    """"""
    flattened_output = {}
    for key in json_data.keys():
        if isinstance(json_data[key], dict):
            get = flatten_json(json_data[key], delimiter)
            for sub_key in get.keys():
                flattened_output[key + delimiter + sub_key] = get[sub_key]
        else:
            flattened_output[key] = json_data[key]

    return flattened_output


def get_detail(fn_name: str):
    """"""
    detail_map = {
        "run_sql": "SQL ",
        "run_assert": "data test ",
        "run_content": "content ",
    }
    return detail_map.get(fn_name, "")


def human_readable(elapsed: float):
    """"""
    minutes, seconds = divmod(elapsed, 60)
    elapsed_minutes = f"{minutes:.0f} minute{'s' if minutes > 1 else ''}"
    elapsed_seconds = f"{seconds:.0f} second{'s' if round(seconds) != 1 else ''}"
    time_separator = " and " if seconds and minutes else ""

    return f"{elapsed_minutes if minutes else ''}{time_separator}{elapsed_seconds if seconds else ''}"


def log_duration(fn: Callable):
    """"""
    functools.wraps(fn)

    def timed_function(*args, **kwargs):
        start_time = timeit.default_timer()
        try:
            result = fn(*args, **kwargs)
        finally:
            elapsed_time = timeit.default_timer() - start_time
            elapsed_formatted = human_readable(elapsed_time)
            message_detail = get_detail(fn.__name__)

            logger.info(
                f"Completed {message_detail}operation in {elapsed_formatted}.\n"
            )
        return result

    return timed_function


def parse_yaml_file(yaml_file_path: str) -> dict:
    """Parse dbt config YAML file to Python dictionary."""
    if not file_exists(yaml_file_path):
        raise DbteaException(
            name="missing-yaml-file",
            title="YAML file set to parse is missing",
            detail="Attempted to parse YAML file at path {}, however this path is not a file".format(
                yaml_file_path
            ),
        )
    with open(yaml_file_path, "r") as yaml_stream:
        yaml_data = yaml.safe_load(yaml_stream) or {}

    return yaml_data


def parse_json_file(json_file_path: str) -> dict:
    """Parse JSON file to Python dictionary."""
    if not file_exists(json_file_path):
        raise DbteaException(
            name="missing-json-file",
            title="JSON file set to parse is missing",
            detail="Attempted to parse JSON file at path {}, however this path is not a file".format(
                json_file_path
            ),
        )
    with open(json_file_path, "r") as json_stream:
        json_data = json.load(json_stream)

    return json_data


def run_cli_command(
    command: Union[List[str], str],
    working_directory: str,
    use_shell: bool = False,
    output_as_text: bool = True,
    capture_output: bool = True,
    **kwargs,
):
    """Execute command line subprocess"""
    result = subprocess.run(
        command,
        shell=use_shell,
        cwd=working_directory,
        text=output_as_text,
        capture_output=capture_output,
        **kwargs,
    )

    if result.stderr:
        raise subprocess.CalledProcessError(
            returncode=result.returncode, cmd=result.args, stderr=result.stderr
        )
    if result.stdout:
        if "Encountered an error" in result.stdout:  # Handle for dbt stdout errors
            logger.error("dbt Error: {}".format(result.stdout))
            raise subprocess.CalledProcessError(
                returncode=result.returncode, cmd=result.args, stderr=result.stdout
            )

        logger.debug("Command Result:\n{}".format(result.stdout))

    return result.stdout


def write_to_yaml_file(data: dict, yaml_file_path: str) -> None:
    """Parse dbt config YAML file to Python dictionary."""
    with open(yaml_file_path, "w") as yaml_stream:
        yaml.safe_dump(data, yaml_stream)
