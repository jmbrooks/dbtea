from dbtea.logger import DBTEA_LOGGER as logger

LOOKML_TYPE_STRING = "string"
LOOKML_TYPE_NUMBER = "number"
LOOKML_TYPE_DATE = "date"
LOOKML_TYPE_DATETIME = "time"
LOOKML_TYPE_BOOL = "yesno"
LOOKML_TYPE_ZIP = "zipcode"

LOOKML_ZIPCODE_FIELD_NAMES = {"zipcode", "zip", "zip_code", "postalcode", "postal_code"}

LOOKML_YESNO_DATA_TYPES = {"bit", "bool", "boolean"}
LOOKML_TIME_DATA_TYPES = {
    "timestamp",
    "timestamp_tz",
    "timestamp_ltz",
    "timestamp_ntz",
    "datetime",
}
LOOKML_DATE_DATA_TYPES = {"date"}
LOOKML_NUMBER_DATA_TYPES = {
    "int",
    "tinyint",
    "smallint",
    "bigint",
    "integer",
    "numeric",
    "number",
    "decimal",
    "float",
    "real",
    "serial",
    "int64",
    "double",
    "double precision",
}


def convert_to_lookml_data_type(
    field_name: str, field_type: str, include_postal_code: bool = False
) -> str:
    """"""
    if include_postal_code and field_name in LOOKML_ZIPCODE_FIELD_NAMES:
        lookml_data_type = LOOKML_TYPE_ZIP
    elif field_type in LOOKML_YESNO_DATA_TYPES:
        lookml_data_type = LOOKML_TYPE_BOOL
    elif field_type in LOOKML_TIME_DATA_TYPES:
        lookml_data_type = LOOKML_TYPE_DATETIME
    elif field_type in LOOKML_DATE_DATA_TYPES:
        lookml_data_type = LOOKML_TYPE_DATE
    elif field_type in LOOKML_NUMBER_DATA_TYPES:
        lookml_data_type = LOOKML_TYPE_NUMBER
    else:
        lookml_data_type = LOOKML_TYPE_STRING

    logger.debug(
        f"Field: {field_name} with data type: {field_type} was mapped to LookML type: {lookml_data_type}"
    )
    return lookml_data_type
