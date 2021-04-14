{% macro coalesce_na(column_name, data_type='str') -%}

coalesce({{ column_name }}, {{ default_na(data_type) }})

{%- endmacro %}
