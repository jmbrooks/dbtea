{% macro fetch_source_rank(column_name, campaign_column) %}
    case
        when lower({{ column_name }}) in ('organization', 'eap', 'united') then 1
        when table_name = 'who_referred_you_question' and lower({{ column_name }} in ('snapchat', 'social media post', 'podcast','tiktok') then 5
        when lower({{ column_name }}) in ('adroll', 'affiliate', 'influencer', 'instagram', 'podcast', 'radio', 'wattpad', 'mktemail', 'ooh', 'reddit', 'storefront', 'print', 'tiktok') OR lower({{ column_name }}) = 'mind diagnostics' then 2
        when lower({{ column_name }}) like '%brand%' then (case when lower({{ column_name }}) like '%seo%' then 7 else 6 end)
        when lower({{ column_name }}) like '%adwords%' then 2
        when lower({{ column_name }}) like '%bing%' then 2
        when lower({{ column_name }}) like '%google%' then 2
        when lower({{ column_name }}) like '%facebook%' then 2
        when lower({{ column_name }}) like '%snapchat%' then 2
        when lower({{ column_name }}) like '%applesearchads_api' then (case when lower({{ campaign_column }}) like '%brand%' then 6 else 2 end)
        when lower({{ column_name }}) in ('ios_other', 'android_other', 'criteo', 'yahoo', 'taboola', 'outbrain') then 2
        when lower({{ column_name }}) = 'groupon' then 2
        when lower({{ column_name }}) = 'pinterest' then 4
        when lower({{ column_name }}) in ('ecounseling', 'e-counseling') then 3
        when lower({{ column_name }}) like '%seo%' then 4
        when lower({{ column_name }}) like '%organic%' then 8
        when lower({{ column_name }}) in ('tv', 'streaming') then 2
        else 9
    end
{% endmacro %}
