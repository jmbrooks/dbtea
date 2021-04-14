{% macro one_hot_encode_flags(table_name, flag_column='flags', flags_table='stg_multi_site__flags') %}
    {%- set flags = dbt_utils.get_query_results_as_dict("select lower(flag_name) as flag_name, flag_value from " ~ ref(flags_table) ~ " where lower(flag_table) = '" ~ table_name ~ "'") -%}

    {%- for flag in flags.FLAG_NAME %}
        case when bitand({{ flag_column }}::int, {{ flags.FLAG_VALUE[loop.index0] }}) = {{ flags.FLAG_VALUE[loop.index0] }} then True else False end as flag_{{ flag }}
        {%- if not loop.last %},{% endif -%}
    {% endfor -%}
{% endmacro %}
