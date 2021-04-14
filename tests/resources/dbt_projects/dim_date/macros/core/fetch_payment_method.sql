{% macro fetch_payment_method(column_name) %}
    case
        when {{ column_name }} is null then '(none specified)'
        when {{ column_name }} = 1 then 'stripe'
        when {{ column_name }} = 2 then 'braintree'
        when {{ column_name }} = 3 then 'paypal'
        when {{ column_name }} = 4 then 'groupon'
        when {{ column_name }} = 5 then 'fake'
        when {{ column_name }} = 6 then 'amazon'
        else '(other)'
    end
{% endmacro %}
