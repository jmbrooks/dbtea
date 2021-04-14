{% macro cents_to_dollars(column_name, scale=2) -%}
    case
        when {{ column_name }} is not null
        then ({{ column_name }} / 100)::number(18, {{ scale }})
        else Null
    end
{%- endmacro %}
