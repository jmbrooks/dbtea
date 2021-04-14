{% macro coalesce_deep_future(column_name, data_type='date') -%}

    {%- if data_type | lower == 'date' -%}
        coalesce({{ column_name }}, to_date('2099-12-31'))

    {%- elif data_type | lower == 'int' -%}
        coalesce({{ column_name }}, 20991231)
    
    {%- endif -%}

{%- endmacro %}
