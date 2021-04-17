import os
from pathlib import Path

from dbtea import utils

current_directory = Path(__file__).parent.absolute()


def test_assemble_basic_path():
    simple_directory = "/Users/SampleUser/"
    simple_file_name = "profiles.yml"
    assembled_path = utils.assemble_path(simple_directory, ".dbt", simple_file_name)

    assert assembled_path == "/Users/SampleUser/.dbt/profiles.yml"


def test_assemble_windows_path():
    root_windows_directory = r"C:\Program Files (x86)\Python"
    second_windows_directory = r"root\tests"
    file_name = "sample.py"
    assembled_path = utils.assemble_path(
        root_windows_directory, second_windows_directory, "unit", file_name
    )

    assert assembled_path == "C:/Program Files (x86)/Python/root/tests/unit/sample.py"


def test_fetch_dbt_basic_project():
    dbt_basic_project_path = os.path.join(
        current_directory, "resources", "dbt_projects", "basic"
    )
    project_path = utils.fetch_dbt_project_directory(
        custom_project_directory=dbt_basic_project_path
    )
    assert project_path.endswith("resources/dbt_projects/basic")
