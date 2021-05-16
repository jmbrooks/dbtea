from configparser import ConfigParser
from pathlib import Path
from typing import Optional

import dbtea.utils as utils
from dbtea.clients.dbt import PROFILES_DIR
from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger

DEFAULT_DBTEA_CONFIG = "dbtea-config.yml"


class DbteaConfig:
    """"""

    def __init__(
        self,
        file_name: str = DEFAULT_DBTEA_CONFIG,
        config_dir: str = PROFILES_DIR,
        config_data: dict = None,
        replace_config_if_exists: bool = True,
        dbt_project: Optional[str] = None,
        looker_project: Optional[str] = None,
        looker_config_path: Optional[str] = None,
        looker_config_section: Optional[str] = None,
        looker_replace_config_if_exists: Optional[bool] = True
    ):
        self.file_name = file_name
        self.config_dir = config_dir
        self.dbt_project = dbt_project
        self.looker_project = looker_project
        self.looker_config_path = looker_config_path or utils.assemble_path(utils.get_home_dir(), ".dbt", "looker.ini")
        self.looker_config_section = looker_config_section or "looker"
        self.looker_config = ConfigParser() if looker_project else None

        if self._config_data_exists() and not replace_config_if_exists:
            self.config_data = utils.parse_yaml_file(self.config_name_and_path)
        else:
            self.config_data = config_data or {}

        if looker_project and not self._config_file_exists(self.looker_config_path) or looker_replace_config_if_exists:
            self.write_looker_config()

        self.write_data_to_file(replace_if_exists=replace_config_if_exists)

    @property
    def config_name_and_path(self) -> str:
        return utils.assemble_path(self.config_dir, self.file_name)

    @classmethod
    def from_config_data(cls, config_data: dict):
        """"""
        return cls(config_data=config_data)

    # @classmethod
    # def from_default_config(self) -> None:
    #     """"""
    #     self.config_data = {
    #         ""
    #     }

    @classmethod
    def from_existing_config_file(cls, local_config_file_path: str):
        """"""
        if utils.file_exists(local_config_file_path):
            return cls(
                file_name=Path(local_config_file_path).name,
                config_dir=Path(local_config_file_path).parent,
                config_data=utils.parse_yaml_file(local_config_file_path),
            )
        else:
            return DbteaException(
                title="invalid-dbtea-config-file-local-path",
                name="Specified Dbtea config local path does not exist",
                detail="You have specified a local config file path to a Dbtea config file which does not exist, "
                "check to confirm file at path: {} exists or any expected environment variables are specified",
            )

    def write_data_to_file(self, replace_if_exists: bool = True) -> None:
        """"""
        if self._config_file_exists() and self._config_data_exists() and not replace_if_exists:
            logger.warning("Dbtea config file already exists, ignoring write config data to file step")
        else:
            logger.info("Creating {} file at path: {}".format(self.file_name, self.config_dir))
            utils.write_to_yaml_file(self.config_data, self.config_name_and_path)

    def read_looker_config(self):
        """"""
        return ConfigParser().read(self.looker_config_path)

    def write_looker_config(self):
        """"""
        logger.info("Writing Looker config file at path: {}".format(self.looker_config_path))
        self.looker_config.add_section(self.looker_config_section)
        for key, value in self.config_data.get(self.dbt_project, {}).items():
            if key.startswith("looker_sdk_"):
                self.looker_config.set(self.looker_config_section, str(key.replace("looker_sdk_", "")), str(value))

        with open(self.looker_config_path, "w") as config_stream:
            self.looker_config.write(config_stream)

    def _config_file_exists(self, file_path: Optional[str] = None) -> bool:
        """"""
        return utils.file_exists(file_path or self.config_name_and_path)

    def _config_data_exists(self) -> bool:
        """"""
        config_data = utils.parse_yaml_file(self.config_name_and_path)
        return True if config_data else False
