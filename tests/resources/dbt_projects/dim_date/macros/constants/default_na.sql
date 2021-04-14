{% macro default_na(data_type='str') -%}

    {%- if data_type | lower == 'str' -%}
        '(not applicable)'

    {%- elif data_type | lower == 'int' -%}
        -1

    {%- elif data_type | lower == 'date' -%}
        to_date('1970-01-01')

    {%- elif data_type | lower == 'datetime' -%}
        to_timestamp('1970-01-01')

    {%- elif data_type | lower == 'date_int' -%}
        19700101

    {%- endif -%}

{%- endmacro %}
