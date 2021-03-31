import lkml


def parse_lookml_file(lookml_file_name: str) -> dict:
    """Parse a LookML file into a dictionary with keys for each of its primary properties and a list of values."""
    with open(lookml_file_name, 'r') as lookml_file_stream:
        lookml_data = lkml.load(lookml_file_stream)

    return lookml_data

result = parse_lookml_file("/Users/johnathanbrooks/PycharmProjects/dbtea/tests/resources/lookml_projects/dim_date/views/dim_date.view.lkml")
print(result)