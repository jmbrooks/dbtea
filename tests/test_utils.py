import os
from pathlib import Path
from dbtea import utils

current_directory = Path(__file__).parent.absolute()


def test_fetch_dbt_basic_project():
    dbt_basic_project_path = os.path.join(current_directory, 'resources/dbt_projects', 'basic')
    project_path = utils.fetch_dbt_project_directory(custom_project_directory=dbt_basic_project_path)
    assert project_path.endswith("tests/dbt_projects/basic")
