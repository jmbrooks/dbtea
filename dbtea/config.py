from pathlib import Path

import dbtea.utils as utils
from dbtea.dbt_client.project import PROFILES_DIR
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
    ):
        self.file_name = file_name
        self.config_dir = config_dir
        self.config_data = config_data

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
        if (
            self._config_file_exists()
            and self._config_data_exists()
            and not replace_if_exists
        ):
            logger.warning(
                "Dbtea config file already exists, ignoring write config data to file step"
            )
        else:
            logger.info(
                "Creating {} file at path: {}".format(self.file_name, self.config_dir)
            )
            utils.write_to_yaml_file(self.config_data, self.config_name_and_path)

    def _config_file_exists(self) -> bool:
        return utils.file_exists(self.config_name_and_path)

    def _config_data_exists(self) -> bool:
        config_data = utils.parse_yaml_file(self.config_name_and_path)
        return True if config_data else False
