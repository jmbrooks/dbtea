"""
Initialize dbt project data.

"""
import dbt.config.project as dbt_project
from dbt.config.profile import PROFILES_DIR

import dbtea.utils as utils
from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger

ARTIFACT_DATA_FILES = {
    "catalog": "catalog.json",
    "manifest": "manifest.json",
    "run_results": "run_results.json",
    "sources": "sources.json",
}
DBT_CLEAN = ["dbt", "clean"]
DBT_COMPILE = ["dbt", "compile"]
DBT_DEBUG = ["dbt", "debug"]
DBT_DEPS = ["dbt", "deps"]
DBT_DOCS_GENERATE = ["dbt", "docs", "generate"]
DBT_DOCS_SERVE = ["dbt", "docs", "serve"]
DBT_LIST = ["dbt", "list"]
DBT_INIT = ["dbt", "init"]
DBT_PARSE = ["dbt", "parse"]
DBT_RPC = ["dbt", "rpc"]
DBT_RUN_OPERATION = ["dbt", "run-operation"]
DBT_RUN = ["dbt", "run"]
DBT_SEED = ["dbt", "seed"]
DBT_SNAPSHOT = ["dbt", "snapshot"]
DBT_SOURCE_SNAPSHOT_FRESHNESS = ["dbt", "source", "snapshot-freshness"]
DBT_TEST = ["dbt", "test"]


class DbtProject(dbt_project.PartialProject):
    """"""

    @property
    def log_path(self):
        return utils.assemble_path(
            self.project_root, self.project_dict.get("log-path", "logs")
        )

    @property
    def profile_path(self):
        return PROFILES_DIR

    @property
    def target_path(self):
        return utils.assemble_path(
            self.project_root, self.project_dict.get("target-path", "target")
        )

    @property
    def catalog_artifact_data(self):
        return self._parse_artifact(ARTIFACT_DATA_FILES["catalog"])

    @property
    def manifest_artifact_data(self):
        return self._parse_artifact(ARTIFACT_DATA_FILES["manifest"])

    @property
    def run_results_artifact_data(self):
        return self._parse_artifact(ARTIFACT_DATA_FILES["run_results"])

    @property
    def sources_artifact_data(self):
        return self._parse_artifact(ARTIFACT_DATA_FILES["sources"])

    def run_dbt_clean(self, *args, **kwargs) -> None:
        """Run `dbt clean` command to remove clean target folders (usually dbt_modules, target) from dbt project."""
        logger.info("Removing dbt clean target folders from dbt project...")
        result = self._dbt_cli_runner(DBT_CLEAN, *args, **kwargs)
        logger.info(result)

    def run_dbt_compile(self, *args, **kwargs) -> None:
        """Run `dbt compile` command to compile dbt models."""
        logger.info("Compiling dbt models...")
        result = self._dbt_cli_runner(DBT_COMPILE, *args, **kwargs)
        logger.info(result)

    def run_dbt_debug(self, *args, **kwargs) -> None:
        """Run `dbt debug` command to check if your dbt_project.yml and profiles.yml files are properly configured."""
        logger.info(
            "Confirming proper dbt project setup, profile and warehouse access..."
        )
        result = self._dbt_cli_runner(DBT_DEBUG, *args, **kwargs)
        logger.info(result)

    def run_dbt_deps(self, require_codegen: bool = False, *args, **kwargs) -> None:
        """Run `dbt deps` command to install dbt project dependencies; the `codegen` package must be included."""
        project_packages_file = utils.assemble_path(self.project_root, "packages.yml")

        if require_codegen:
            if not utils.file_exists(project_packages_file):
                raise FileExistsError(
                    "You must have a packages.yml file specified in your project"
                )

            package_data = utils.parse_yaml_file(project_packages_file)

            package_list = [
                entry.get("package") for entry in package_data.get("packages", {})
            ]
            if "fishtown-analytics/codegen" not in package_list:
                raise ValueError(
                    "You have not brought the codegen dbt package into your project! You must include the "
                    "package 'fishtown-analytics/codegen' in your `packages.yml` file to codegen in bulk."
                )

        logger.info("Fetching dbt project package dependencies...")
        result = self._dbt_cli_runner(DBT_DEPS, *args, **kwargs)
        logger.info(result)

    def run_dbt_docs_generate(self, *args, **kwargs) -> None:
        """Run `dbt docs generate` command to generate dbt documentation artifacts."""
        logger.info("Generating dbt documentation artifacts...")
        result = self._dbt_cli_runner(DBT_DOCS_GENERATE, *args, **kwargs)
        logger.info(result)

    def run_dbt_docs_serve(self, *args, **kwargs) -> None:
        """Run `dbt docs serve` command to view dbt documentation."""
        logger.info("Serving dbt documentation site...")
        result = self._dbt_cli_runner(DBT_DOCS_SERVE, *args, **kwargs)
        logger.info(result)

    def run_dbt_list(self, *args, **kwargs) -> None:
        """Run `dbt list` (ls) command to list all resources within the dbt project."""
        logger.info("Listing dbt project resources...")
        result = self._dbt_cli_runner(DBT_LIST, *args, **kwargs)
        logger.info(result)

    def run_dbt_init(self, *args, **kwargs) -> None:
        """Run `dbt init` command to create a base dbt project."""
        logger.info("Initialize a base dbt project...")
        result = self._dbt_cli_runner(DBT_INIT, *args, **kwargs)
        logger.info(result)

    def run_dbt_parse(self, *args, **kwargs) -> None:
        """Run `dbt parse` command to provide information on performance."""
        logger.info("Parsing dbt project for performance details...")
        result = self._dbt_cli_runner(DBT_PARSE, *args, **kwargs)
        logger.info(result)

    def run_dbt_rpc(self, *args, **kwargs) -> None:
        """Run `dbt rpc` command to spin up an RPC server."""
        logger.info("Starting dbt RPC server...")
        result = self._dbt_cli_runner(DBT_RPC, *args, **kwargs)
        logger.info(result)

    def run_dbt_run_operation(
        self, macro_name: str, macro_args: dict = None, *args, **kwargs
    ) -> None:
        """Run `dbt run-operation` command to run dbt macros."""
        logger.info("Executing dbt macro operation {}...".format(macro_name))
        operation_with_macro = DBT_RUN_OPERATION.copy()
        operation_with_macro.append(macro_name)
        if macro_args:
            operation_with_macro.append(f"--args '{macro_args}'")

        result = self._dbt_cli_runner(operation_with_macro, *args, **kwargs)
        logger.info(result)

    def run_dbt_run(self, *args, **kwargs) -> None:
        """Run `dbt run` command to run dbt models."""
        logger.info("Running dbt models...")
        result = self._dbt_cli_runner(DBT_RUN, *args, **kwargs)
        logger.info(result)

    def run_dbt_seed(self, *args, **kwargs) -> None:
        """Run `dbt seed` command to upload seed data."""
        logger.info("Uploading dbt seed data files to data warehouse...")
        result = self._dbt_cli_runner(DBT_SEED, *args, **kwargs)
        logger.info(result)

    def run_dbt_snapshot(self, *args, **kwargs) -> None:
        """Run `dbt snapshot` command to execute dbt snapshots."""
        logger.info("Running dbt snapshots...")
        result = self._dbt_cli_runner(DBT_SNAPSHOT, *args, **kwargs)
        logger.info(result)

    def run_dbt_source_snapshot_freshness(self, *args, **kwargs) -> None:
        """Run `dbt source snapshot-freshness` command to get freshness of data sources."""
        logger.info("Checking freshness of data source tables...")
        result = self._dbt_cli_runner(DBT_SOURCE_SNAPSHOT_FRESHNESS, *args, **kwargs)
        logger.info(result)

    def run_dbt_test(self, *args, **kwargs) -> None:
        """Run `dbt test` command to run dbt models."""
        logger.info("Running dbt tests to validate models...")
        result = self._dbt_cli_runner(DBT_TEST, *args, **kwargs)
        logger.info(result)

    def _dbt_cli_runner(self, input_command_as_list: list, *args, **kwargs):
        """Run dbt CLI command based on input options."""
        arg_flags = list()
        kwarg_flags = list()
        if args:
            for flag in args:
                arg_flags.append(f"--{flag}")
            input_command_as_list.extend(arg_flags)
        if kwargs:
            for flag, flag_value in kwargs.items():
                kwarg_flags.append(f"--{flag} '{flag_value}'")
            input_command_as_list.extend(kwarg_flags)

        input_command = " ".join(input_command_as_list)

        logger.info("Running dbt command: ".format(" ".join(input_command_as_list)))
        return utils.run_cli_command(
            input_command,
            working_directory=self.project_root,
            use_shell=True,
            output_as_text=True,
            capture_output=True,
        )

    def _parse_artifact(self, artifact_file: str):
        """"""
        if artifact_file not in ARTIFACT_DATA_FILES.values():
            logger.warning(
                "You have specified an artifact file which is not in the list of known dbt artifacts"
            )
        artifact_path = utils.assemble_path(
            self.project_root, self.target_path, artifact_file
        )
        if not utils.file_exists(artifact_path):
            raise DbteaException(
                name="artifact-file-missing",
                title="Artifact file {} is missing".format(artifact_file),
                detail="There is no artifact {} at path {}. You may not have yet generated this artifact and "
                "need to run models, source freshness or docs generation".format(
                    artifact_file, artifact_path
                ),
            )
        return utils.parse_json_file(artifact_path)
