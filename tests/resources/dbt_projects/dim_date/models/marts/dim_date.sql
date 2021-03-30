{{ config(materialized='table') }}

{% set current_time = dbt_utils.current_timestamp() %}

with seed_dim_date as (

  select * from {{ ref('seed_dim_date') }}

),

final as (

    select
        {{ to_date_key('calendar_date') }} as date_key,
        calendar_date,

        day_of_week,
        day_of_week_name,

        day_of_month,
        week_of_month,
        calendar_month,

        day_of_quarter,
        week_of_quarter,
        month_of_quarter,
        calendar_quarter,

        day_of_year,
        week_of_year,
        month_of_year,
        quarter_of_year,
        calendar_year,

        is_leap_year,
        is_weekday,
        is_holiday,
        is_workday,

        days_in_month,
        days_in_quarter,
        days_in_year,
        day_of_week_in_month,
        day_of_week_in_quarter,
        day_of_week_in_year,

        first_date_of_week,
        last_date_of_week,
        first_date_of_month,
        last_date_of_month,
        first_date_of_quarter,
        last_date_of_quarter,
        first_date_of_year,
        last_date_of_year,

        {{ to_date_key('calendar_date') }}              as year_month_day,
        {{ to_date_key('calendar_date', 'month') }}     as year_month,
        {{ to_date_key('calendar_date', 'quarter') }}   as year_quarter,
        'Calendar Day'                                  as custom_date_detail,

        {{ default_na('datetime') }}                    as row_valid_from_time,
        {{ coalesce_deep_future('Null') }}              as row_valid_to_time,
        True                                            as is_row_currently_valid,
        {{ dbt_utils.surrogate_key(['date_key'])}}      as scd_unique_key,
        current_timestamp()                             as inserted_at
    from
        seed_dim_date
    where
        calendar_date >= '{{ var("analysis_start_date") }}'
        and calendar_date <= date(datefromparts(extract(year from {{ current_time }}), 12, 31))

    union all

    select
        {{ coalesce_deep_future('Null', 'int') }}       as date_key,
        {{ coalesce_deep_future('Null') }}              as calendar_date,

        dayofweek(calendar_date)                        as day_of_week,
        case day_of_week
          when 0 then 'Sunday'
          when 1 then 'Monday'
          when 2 then 'Tuesday'
          when 3 then 'Wednesday'
          when 4 then 'Thursday'
          when 5 then 'Friday'
          when 6 then 'Saturday'
        end                                             as day_of_week_name,

        dayofmonth(calendar_date)                       as day_of_month,
        NULL                                            as week_of_month,
        NULL                                            as calendar_month,

        NULL                                            as day_of_quarter,
        NULL                                            as week_of_quarter,
        NULL                                            as month_of_quarter,
        NULL                                            as calendar_quarter,

        NULL                                            as day_of_year,
        NULL                                            as week_of_year,
        NULL                                            as month_of_year,
        NULL                                            as quarter_of_year,
        NULL                                            as calendar_year,

        FALSE                                           as is_leap_year,
        FALSE                                           as is_weekday,
        FALSE                                           as is_holiday,
        FALSE                                           as is_workday,

        31                                              as days_in_month,
        NULL                                            as days_in_quarter,
        365                                             as days_in_year,
        NULL                                            as day_of_week_in_month,
        NULL                                            as day_of_week_in_quarter,
        NULL                                            as day_of_week_in_year,

        NULL                                            as first_date_of_week,
        NULL                                            as last_date_of_week,
        NULL                                            as first_date_of_month,
        NULL                                            as last_date_of_month,
        NULL                                            as first_date_of_quarter,
        NULL                                            as last_date_of_quarter,
        NULL                                            as first_date_of_year,
        NULL                                            as last_date_of_year,

        {{ coalesce_deep_future('Null', 'int') }}       as year_month_day,
        {{ to_date_key(coalesce_deep_future('Null'), 'month') }} as year_month,
        {{ to_date_key(coalesce_deep_future('Null'), 'quarter') }} as year_quarter,
        'Spans Multiple Dates'                          as custom_date_detail,

        {{ default_na('datetime') }}                    as row_valid_from_time,
        {{ coalesce_deep_future('Null') }}              as row_valid_to_time,
        True                                            as is_row_currently_valid,
        {{ dbt_utils.surrogate_key(['date_key']) }}     as scd_unique_key,
        current_timestamp()                             as inserted_at

    union all

    select
        {{ default_na('date_int') }}                    as date_key,
        {{ default_na('date') }}                        as calendar_date,

        dayofweek(calendar_date)                        as day_of_week,
        case day_of_week
          when 0 then 'Sunday'
          when 1 then 'Monday'
          when 2 then 'Tuesday'
          when 3 then 'Wednesday'
          when 4 then 'Thursday'
          when 5 then 'Friday'
          when 6 then 'Saturday'
        end                                             as day_of_week_name,

        dayofmonth(calendar_date)                       as day_of_month,
        NULL                                            as week_of_month,
        NULL                                            as calendar_month,

        NULL                                            as day_of_quarter,
        NULL                                            as week_of_quarter,
        NULL                                            as month_of_quarter,
        NULL                                            as calendar_quarter,

        NULL                                            as day_of_year,
        NULL                                            as week_of_year,
        NULL                                            as month_of_year,
        quarter(calendar_date)                          as quarter_of_year,
        year(calendar_date)                             as calendar_year,

        FALSE                                           as is_leap_year,
        FALSE                                           as is_weekday,
        FALSE                                           as is_holiday,
        FALSE                                           as is_workday,

        31                                              as days_in_month,
        NULL                                            as days_in_quarter,
        365                                             as days_in_year,
        NULL                                            as day_of_week_in_month,
        NULL                                            as day_of_week_in_quarter,
        NULL                                            as day_of_week_in_year,

        NULL                                            as first_date_of_week,
        NULL                                            as last_date_of_week,
        NULL                                            as first_date_of_month,
        NULL                                            as last_date_of_month,
        NULL                                            as first_date_of_quarter,
        NULL                                            as last_date_of_quarter,
        NULL                                            as first_date_of_year,
        NULL                                            as last_date_of_year,

        {{ default_na('date_int') }}                    as year_month_day,
        {{ to_date_key(default_na('date'), 'month') }}  as year_month,
        {{ to_date_key(default_na('date'), 'quarter') }} as year_quarter,
        'Not Applicable or Unknown Date'                as custom_date_detail,

        {{ default_na('datetime') }}                    as row_valid_from_time,
        {{ coalesce_deep_future('Null') }}              as row_valid_to_time,
        True                                            as is_row_currently_valid,
        {{ dbt_utils.surrogate_key(['date_key']) }}     as scd_unique_key,
        current_timestamp()                             as inserted_at

)

select * from final
