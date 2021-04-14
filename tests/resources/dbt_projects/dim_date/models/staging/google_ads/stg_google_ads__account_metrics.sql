with source as (

    select * from {{ source('google_ads', 'account_metrics') }}

),

renamed as (

    select
        {{ dbt_utils.surrogate_key(['customer_id', 'report_date']) }} as account_metric_id,
        customer_id as account_id,
        report_date,
        impressions as daily_impressions,
        round(cost / 1000000, 2) as daily_cost,
        kbc_synced_at

    from source

)

select * from renamed
