{% macro parse_ua(column_name, parsing_field='browser') %}
    case
        when '{{ parsing_field }}' = 'browser'
            then case
                when {{ column_name }} ilike '%537.36 Edge%' then 'microsoft edge'
                when {{ column_name }} ilike '%Firefox/%' then 'firefox'
                when {{ column_name }} ilike '%CriOS%' then 'chrome ios'
                when {{ column_name }} ilike '%Chrome/%' then 'chrome'
                when {{ column_name }} ilike '%MSIE %' then 'ie'
                when {{ column_name }} ilike '%MSIE+%' then 'ie'
                when {{ column_name }} ilike '%Trident%' then 'ie'
                when {{ column_name }} ilike '%iPhone%' then 'iphone safari'
                when {{ column_name }} ilike '%iPad%' then 'ipad safari'
                when {{ column_name }} ilike '%Opera%' then 'opera'
                when {{ column_name }} ilike '%BlackBerry%' AND {{ column_name }} ilike '%Version/%' then 'blackberry webkit'
                when {{ column_name }} ilike '%BlackBerry%' then 'blackberry'
                when {{ column_name }} ilike '%Android%' then 'android'
                when {{ column_name }} ilike '%Safari%' then 'safari'
                when {{ column_name }} ilike '%bot%' then 'bot'
                when {{ column_name }} ilike '%http://%' then 'bot'
                when {{ column_name }} ilike '%www.%' then 'bot'
                when {{ column_name }} ilike '%Wget%' then 'bot'
                when {{ column_name }} ilike '%curl%' then 'bot'
                when {{ column_name }} ilike '%urllib%' then 'bot'
                else 'unknown'
            end
        when '{{ parsing_field }}' = 'device'
            then case
                when {{ column_name }} ilike '%android_betterhelp_app%' then 'android app'
                when {{ column_name }} ilike '%web_view_ios_app%' then 'ios app'
                when {{ column_name }} ilike '%iPhone%' then 'iphone'
                when {{ column_name }} ilike '%iPod%' then 'ipod'
                when {{ column_name }} ilike '%iPad%' then 'ipad'
                when {{ column_name }} ilike '%Android%' then 'android'
                when {{ column_name }} ilike '%BlackBerry%' then 'blackberry'
                when {{ column_name }} ilike '%IEMobile/%' then 'iemobile'
                when {{ column_name }} ilike '%/Mobile%' then 'mobile_other'
                else 'desktop'
            end
        when '{{ parsing_field }}' = 'device_type'
            then case
                when {{ column_name }} ilike '%/Mobile%'
                  or {{ column_name }} ilike '%iPhone%'
                  or {{ column_name }} ilike '%iPod%'
                  or {{ column_name }} ilike '%iPad%'
                  or {{ column_name }} ilike '%Android%'
                  or {{ column_name }} ilike '%BlackBerry%'
                  or {{ column_name }} ilike '%IEMobile/%'
                  then 'mobile'
                else 'desktop'
            end
    end
{% endmacro %}
