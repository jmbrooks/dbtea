from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import lkml
import looker_sdk

import dbtea.utils as utils
from dbtea.exceptions import DbteaException
from dbtea.logger import DBTEA_LOGGER as logger

OUTPUT_TO_OPTIONS = {"stdout", "file"}

LOOKML_DIMENSION = "dimension"
LOOKML_DIMENSION_GROUP = "dimension_group"
LOOKML_MEASURE = "measure"
LOOKML_SET = "set"

LOOKML_DIMENSION_GROUP_TYPES = {"duration", "time"}

LOOKML_ZIPCODE_FIELD_NAMES = {"zipcode", "zip", "zip_code", "postalcode", "postal_code"}
VALID_LOOKML_VIEW_PROPERTIES = {
    "name",
    "label",
    "extends",
    "extension",
    "sql_table_name",
    "derived_table",
    "required_access_grants",
    "suggestions",
    "parameters",
    "parameter",
    "dimensions",
    "dimension",
    "dimension_groups",
    "dimension_group" "measures",
    "measure",
    "sets",
    "set",
}
VALID_LOOKML_DIMENSION_PROPERTIES = {
    "name",
    "action",
    "allow_fill",
    "alpha_sort",
    "bypass_suggest_restrictions",
    "can_filter",
    "case",
    "case_sensitive",
    "datatype",
    "drill_fields",
    "end_location_field",
    "fanout_on",
    "full_suggestions",
    "group_label",
    "group_item_label",
    "html",
    "label_from_parameter",
    "link",
    "map_layer_name",
    "order_by_field",
    "primary_key",
    "required_fields",
    "skip_drill_filter",
    "start_location_field",
    "suggestions",
    "suggest_persist_for",
    "style",
    "sql",
    "sql_end",
    "sql_start",
    "tiers",
    "sql_longitude",
    "sql_latitude",
    "string_datatype",
    "units",
    "value_format",
    "value_format_name",
    "alias",
    "convert_tz",
    "description",
    "hidden",
    "label",
    "required_access_grants",
    "suggestable",
    "tags",
    "type",
    "suggest_dimension",
    "suggest_explore",
    "view_label",
}


class LookmlProject:
    """"""

    def __init__(self, project_id: str, config_file_path: Optional[str] = None, config_section: str = "looker"):
        config_path = config_file_path if config_file_path \
            else utils.assemble_path(utils.get_home_dir(), ".dbt", "looker.ini")
        super().__init__(id=project_id)
        self.api_client = looker_sdk.init31(config_file=config_path, section=config_section)
        self._project = self.api_client.project(project_id)

    @property
    def name(self):
        return self._project.name


@dataclass
class LookmlFile:
    """"""

    name: str
    lookml_type: str
    directory_path: str
    lookml_data: Optional[dict] = None
    lookml_objects: Optional[dict] = None

    @classmethod
    def from_local_file(cls, looker_project_root: str, file_relative_path: str):
        """"""
        full_project_path = utils.assemble_path(looker_project_root, file_relative_path)
        path_suffixes = Path(full_project_path).suffixes
        lookml_file_type = path_suffixes[0] if len(path_suffixes) > 1 else "generic"
        directory, file_name = (
            Path(full_project_path).parent,
            Path(full_project_path).stem,
        )

        with open(full_project_path, "r") as local_file_stream:
            return cls(
                file_name,
                lookml_file_type,
                directory_path=directory,
                lookml_data=lkml.load(local_file_stream),
            )

    @classmethod
    def from_lookml_string(
        cls,
        name: str,
        lookml_type: str,
        directory_path: str = "./",
        lookml_string: str = None,
    ):
        """"""
        return cls(
            name,
            lookml_type,
            directory_path=directory_path,
            lookml_data=lkml.load(lookml_string),
        )

    @property
    def lookml_file_name(self) -> str:
        """"""
        if self.lookml_type.lower() == "generic":
            return f"{self.name}.lkml"
        else:
            return f"{self.name}.{self.lookml_type}.lkml"

    @property
    def lookml_file_name_and_path(self) -> str:
        """"""
        return utils.assemble_path(self.directory_path, self.lookml_file_name)

    @property
    def lookml_string(self) -> str:
        """"""
        return lkml.dump(self.lookml_data)

    def set_lookml_data(self, lookml_data: dict):
        """"""
        self.lookml_data = lookml_data

    def add_lookml_object(self, lookml_object: str, object_type: str):
        """"""
        if not self.lookml_objects.get(object_type):
            self.lookml_objects[object_type] = [lookml_object]
        else:
            self.lookml_objects[object_type].append(lookml_object)
        return self.lookml_objects

    def read_data_from_file(self, local_lookml_project_path: str) -> dict:
        """Parse a LookML file into a dictionary with keys for each of its primary properties and a list of values."""
        logger.info(
            "Parsing data from local LookML file {}".format(
                self.lookml_file_name_and_path
            )
        )
        with open(
            utils.assemble_path(
                local_lookml_project_path, self.lookml_file_name_and_path
            ),
            "r",
        ) as lookml_file:
            return lkml.load(lookml_file)

    def write_data_to_file(self, local_lookml_project_path: str) -> None:
        """"""
        with open(
            utils.assemble_path(
                local_lookml_project_path, self.lookml_file_name_and_path
            )
        ) as lookml_file:
            lookml_file.write(self.lookml_string)


class LookmlModel(LookmlFile):
    """"""

    def __init__(self, name: str, directory_path: str = None, model_data: dict = None):
        """"""
        super().__init__(
            name, "model", directory_path=directory_path, lookml_data=model_data
        )

    @classmethod
    def assemble_model(
        cls,
        model_name: str,
        directory_path: str,
        connection: str = None,
        label: str = None,
        includes: list = None,
        explores: List[dict] = None,
        access_grants: List[dict] = None,
        tests: List[dict] = None,
        datagroups: List[dict] = None,
        map_layers: List[dict] = None,
        named_value_formats: List[dict] = None,
        fiscal_month_offset: int = None,
        persist_for: str = None,
        persist_with: str = None,
        week_start_day: str = None,
        case_sensitive: bool = True,
    ):
        """"""
        assembled_model_dict = dict()
        logger.info("Creating LookML Model: {}".format(model_name))

        # Add optional model options
        if connection:
            assembled_model_dict["connection"] = connection
        if label:
            assembled_model_dict["label"] = label
        if includes:
            assembled_model_dict["includes"] = includes
        if persist_for:
            assembled_model_dict["persist_for"] = persist_for
        if persist_with:
            assembled_model_dict["persist_with"] = persist_with
        if fiscal_month_offset:
            assembled_model_dict["fiscal_month_offset"] = fiscal_month_offset
        if week_start_day:
            assembled_model_dict["week_start_day"] = week_start_day
        if not case_sensitive:
            assembled_model_dict["case_sensitive"] = "no"

        # Add body of Model
        if datagroups:
            assembled_model_dict["datagroups"] = datagroups
        if access_grants:
            assembled_model_dict["access_grants"] = access_grants
        if explores:
            assembled_model_dict["explores"] = explores
        if named_value_formats:
            assembled_model_dict["named_value_formats"] = named_value_formats
        if map_layers:
            assembled_model_dict["map_layers"] = map_layers
        if tests:
            assembled_model_dict["tests"] = tests

        return super().__init__(
            model_name,
            "model",
            directory_path=directory_path,
            lookml_data=assembled_model_dict,
        )

    @property
    def explores(self) -> Optional[List[dict]]:
        return self.lookml_data.get("explores")


class LookmlView(LookmlFile):
    """"""

    def __init__(self, name: str, directory_path: str = None, view_data: dict = None):
        """"""
        super().__init__(
            name, "view", directory_path=directory_path, lookml_data=view_data
        )

    @classmethod
    def assemble_view(
        cls,
        view_name: str,
        sql_table_name: str = None,
        derived_table: str = None,
        dimensions: List[dict] = None,
        dimension_groups: List[dict] = None,
        measures: List[dict] = None,
        sets: List[dict] = None,
        parameters: List[dict] = None,
        label: str = None,
        required_access_grants: list = None,
        extends: str = None,
        extension_is_required: bool = False,
        include_suggestions: bool = True,
    ):
        assembled_view_dict = {"view": {"name": view_name}}
        logger.info("Creating LookML View: {}".format(view_name))

        # Validate inputs
        if not sql_table_name and not derived_table and not extends:
            raise DbteaException(
                name="missing-lookml-view-properties",
                title="Missing Necessary LookML View Properties",
                detail="Created LookML Views must specify either a `sql_table_name`, `derived_table` or `extends` in order "
                "to properly specify the view source",
            )

        # Add optional view options as needed
        if label:
            assembled_view_dict["view"]["label"] = label
        if extends:
            assembled_view_dict["view"]["extends"] = extends
        if extension_is_required:
            assembled_view_dict["view"]["extension"] = "required"
        if sql_table_name:
            assembled_view_dict["view"]["sql_table_name"] = sql_table_name
        if derived_table:
            assembled_view_dict["view"]["derived_table"] = derived_table
        if required_access_grants:
            assembled_view_dict["view"][
                "required_access_grants"
            ] = required_access_grants
        if not include_suggestions:
            assembled_view_dict["view"]["suggestions"] = "no"

        # Add body of View
        if parameters:
            assembled_view_dict["view"]["parameters"] = parameters
        if dimensions:
            assembled_view_dict["view"]["dimensions"] = dimensions
        if dimension_groups:
            assembled_view_dict["view"]["dimension_groups"] = dimension_groups
        if measures:
            assembled_view_dict["view"]["measures"] = measures
        if sets:
            assembled_view_dict["view"]["sets"] = sets

        return lkml.dump(assembled_view_dict)

    @property
    def dimensions(self) -> Optional[List[dict]]:
        return self.lookml_data.get("dimensions")

    @property
    def dimension_groups(self) -> Optional[List[dict]]:
        return self.lookml_data.get("dimension_groups")

    @property
    def measures(self) -> Optional[List[dict]]:
        return self.lookml_data.get("measures")

    @property
    def sets(self) -> Optional[List[dict]]:
        return self.lookml_data.get("sets")


def create_lookml_model(
    model_name: str,
    output_to: str = "stdout",
    connection: str = None,
    label: str = None,
    includes: list = None,
    explores: List[dict] = None,
    access_grants: List[dict] = None,
    tests: List[dict] = None,
    datagroups: List[dict] = None,
    map_layers: List[dict] = None,
    named_value_formats: List[dict] = None,
    fiscal_month_offset: int = None,
    persist_for: str = None,
    persist_with: str = None,
    week_start_day: str = None,
    case_sensitive: bool = True,
    output_directory: str = None,
) -> Optional[str]:
    """"""
    assembled_model_dict = dict()
    logger.info("Creating LookML Model: {}".format(model_name))

    # Validate inputs
    if output_to not in OUTPUT_TO_OPTIONS:
        raise DbteaException(
            name="invalid-lookml-model-properties",
            title="Invalid LookML Model Properties",
            detail="You must choose a valid output_to option from the following: {}".format(
                OUTPUT_TO_OPTIONS
            ),
        )
    if output_to == "file" and not output_directory:
        raise DbteaException(
            name="missing-output-directory",
            title="No Model Output Directory Specified",
            detail="You must include an output_directory param if outputting model to a file",
        )

    # Add optional model options
    if connection:
        assembled_model_dict["connection"] = connection
    if label:
        assembled_model_dict["label"] = label
    if includes:
        assembled_model_dict["includes"] = includes
    if persist_for:
        assembled_model_dict["persist_for"] = persist_for
    if persist_with:
        assembled_model_dict["persist_with"] = persist_with
    if fiscal_month_offset:
        assembled_model_dict["fiscal_month_offset"] = fiscal_month_offset
    if week_start_day:
        assembled_model_dict["week_start_day"] = week_start_day
    if not case_sensitive:
        assembled_model_dict["case_sensitive"] = "no"

    # Add body of Model
    if datagroups:
        assembled_model_dict["datagroups"] = datagroups
    if access_grants:
        assembled_model_dict["access_grants"] = access_grants
    if explores:
        assembled_model_dict["explores"] = explores
    if named_value_formats:
        assembled_model_dict["named_value_formats"] = named_value_formats
    if map_layers:
        assembled_model_dict["map_layers"] = map_layers
    if tests:
        assembled_model_dict["tests"] = tests

    if output_to == "stdout":
        return lkml.dump(assembled_model_dict)
    else:
        model_file_name = utils.assemble_path(
            output_directory, model_name + ".model.lkml"
        )
        with open(model_file_name, "w") as output_stream:
            output_stream.write(lkml.dump(assembled_model_dict))


def create_lookml_view(
    view_name: str,
    sql_table_name: str = None,
    derived_table: str = None,
    dimensions: List[dict] = None,
    dimension_groups: List[dict] = None,
    measures: List[dict] = None,
    sets: List[dict] = None,
    parameters: List[dict] = None,
    label: str = None,
    required_access_grants: list = None,
    extends: str = None,
    extension_is_required: bool = False,
    include_suggestions: bool = True,
) -> str:
    """"""
    assembled_view_dict = {"view": {"name": view_name}}
    logger.info("Creating LookML View: {}".format(view_name))

    # Validate inputs
    if not sql_table_name and not derived_table and not extends:
        raise DbteaException(
            name="missing-lookml-view-properties",
            title="Missing Necessary LookML View Properties",
            detail="Created LookML Views must specify either a `sql_table_name`, `derived_table` or `extends` in order "
            "to properly specify the view source",
        )

    # Add optional view options as needed
    if label:
        assembled_view_dict["view"]["label"] = label
    if extends:
        assembled_view_dict["view"]["extends"] = extends
    if extension_is_required:
        assembled_view_dict["view"]["extension"] = "required"
    if sql_table_name:
        assembled_view_dict["view"]["sql_table_name"] = sql_table_name
    if derived_table:
        assembled_view_dict["view"]["derived_table"] = derived_table
    if required_access_grants:
        assembled_view_dict["view"]["required_access_grants"] = required_access_grants
    if not include_suggestions:
        assembled_view_dict["view"]["suggestions"] = "no"

    # Add body of View
    if parameters:
        assembled_view_dict["view"]["parameters"] = parameters
    if dimensions:
        assembled_view_dict["view"]["dimensions"] = dimensions
    if dimension_groups:
        assembled_view_dict["view"]["dimension_groups"] = dimension_groups
    if measures:
        assembled_view_dict["view"]["measures"] = measures
    if sets:
        assembled_view_dict["view"]["sets"] = sets

    return lkml.dump(assembled_view_dict)


def parse_lookml_file(lookml_file_name: str) -> dict:
    """Parse a LookML file into a dictionary with keys for each of its primary properties and a list of values."""
    logger.info("Parsing data from LookML file {}".format(lookml_file_name))
    with open(lookml_file_name, "r") as lookml_file_stream:
        lookml_data = lkml.load(lookml_file_stream)

    return lookml_data


def to_lookml(
    data: dict,
    output_to: str = "stdout",
    output_file: str = None,
    lookml_file_type: str = None,
    output_directory: str = None,
) -> Optional[str]:
    """"""
    if output_to == "stdout":
        return lkml.dump(data)
    else:
        output_file = (
            utils.assemble_path(
                output_directory, output_file + "." + lookml_file_type + ".lkml"
            )
            if lookml_file_type
            else utils.assemble_path(output_directory, output_file + ".lkml")
        )
        with open(output_file, "w") as output_stream:
            output_stream.write(lkml.dump(data))


def dbt_model_schemas_to_lookml_views(dbt_models_data: List[dict]) -> dict:
    """"""
    lookml_views_dbt_data = dbt_models_data

    for model_data in lookml_views_dbt_data:
        if "columns" in model_data:
            model_data["dimensions"] = list()
            model_data["dimension_groups"] = list()
            invalid_column_properties = list()

            for index, column_data in enumerate(model_data["columns"]):
                for column_property_key in column_data.keys():
                    if column_property_key not in VALID_LOOKML_DIMENSION_PROPERTIES:
                        invalid_column_properties.append(column_property_key)
                for invalid_column_property in invalid_column_properties:
                    logger.debug(
                        "Removing property invalid for LookML for dimension {}: {}".format(
                            model_data.get("name"), invalid_column_property
                        )
                    )
                    if model_data["columns"][index].get(invalid_column_property):
                        del model_data["columns"][index][invalid_column_property]

                if column_data.get("type") in LOOKML_DIMENSION_GROUP_TYPES:
                    column_data.update({"sql": "${TABLE}." + column_data.get("name")})
                    model_data["dimension_groups"].append(column_data)
                else:
                    column_data.update({"sql": "${TABLE}." + column_data.get("name")})
                    model_data["dimensions"].append(column_data)
                # model_data["dimensions"][index]["sql"] = "${TABLE}." + column_data.get("name")

            del model_data["columns"]

        if "alias" in model_data:
            model_data["sql_table_name"] = model_data["alias"]
        else:
            model_data["sql_table_name"] = model_data.get(
                "name"
            )  # TODO: Needs to be fully qualified name]

        # Process model-level meta fields
        if "meta" in model_data:
            for meta_key, meta_value in model_data["meta"].items():
                if meta_key[:7] == "looker_" or meta_key[:7] == "lookml_":
                    model_data[meta_key[7:]] = model_data["meta"][meta_key]

        invalid_properties = list()
        for model_property in model_data.keys():
            if model_property not in VALID_LOOKML_VIEW_PROPERTIES:
                invalid_properties.append(model_property)
        for invalid_property in invalid_properties:
            logger.debug(
                "Removing property invalid for LookML for view {}: {}".format(
                    model_data.get("name"), invalid_property
                )
            )
            del model_data[invalid_property]

    return {"views": lookml_views_dbt_data}
