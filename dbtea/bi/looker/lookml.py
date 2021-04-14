import os
from typing import List, Union

import lkml

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
    "name", "label", "extends", "extension", "sql_table_name", "derived_table", "required_access_grants", "suggestions",
    "parameters", "parameter", "dimensions", "dimension", "dimension_groups", "dimension_group" "measures", "measure",
    "sets", "set"
}
VALID_LOOKML_DIMENSION_PROPERTIES = {
    "name", "action", "allow_fill", "alpha_sort", "bypass_suggest_restrictions", "can_filter", "case", "case_sensitive",
    "datatype", "drill_fields", "end_location_field", "fanout_on", "full_suggestions", "group_label",
    "group_item_label", "html", "label_from_parameter", "link", "map_layer_name", "order_by_field", "primary_key",
    "required_fields", "skip_drill_filter", "start_location_field", "suggestions", "suggest_persist_for", "style",
    "sql", "sql_end", "sql_start", "tiers", "sql_longitude", "sql_latitude", "string_datatype", "units", "value_format",
    "value_format_name", "alias", "convert_tz", "description", "hidden", "label", "required_access_grants",
    "suggestable", "tags", "type", "suggest_dimension", "suggest_explore", "view_label"
}


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
) -> Union[None, str]:
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
        model_file_name = os.path.join(output_directory, model_name + ".model.lkml")
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


def to_lookml(data: dict, output_to: str = "stdout", output_file: str = None,
              lookml_file_type: str = None, output_directory: str = None) -> Union[None, str]:
    """"""
    if output_to == "stdout":
        return lkml.dump(data)
    else:
        output_file = os.path.join(output_directory, output_file + "." + lookml_file_type + ".lkml") \
            if lookml_file_type else os.path.join(output_directory, output_file + ".lkml")
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
                    logger.debug("Removing property invalid for LookML for dimension {}: {}".format(
                        model_data.get("name"), invalid_column_property))
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
            model_data["sql_table_name"] = model_data.get("name")  # TODO: Needs to be fully qualified name]

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
            logger.debug("Removing property invalid for LookML for view {}: {}".format(
                model_data.get("name"), invalid_property))
            del model_data[invalid_property]

    return {"views": lookml_views_dbt_data}
