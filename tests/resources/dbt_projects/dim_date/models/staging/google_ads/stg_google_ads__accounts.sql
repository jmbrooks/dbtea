with source as (

    select * from {{ source('google_ads', 'accounts') }}

),

renamed as (

    select
        id as google_ads_account_id,
        client_customer as account_url,
        descriptive_name as account_descriptive_name,
        upper(currency_code) as currency_code,
        timezone,
        hierarchy_level as account_hierarchy_level,
        is_hidden as is_hidden_account,
        is_manager_account,
        is_test_account,
        kbc_synced_at

    from source

)

select * from renamed
