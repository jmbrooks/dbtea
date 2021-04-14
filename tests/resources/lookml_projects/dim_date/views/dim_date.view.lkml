view: dim_date {
  label: "Client"
  sql_table_name: bh_dev.dbt_jbrooks.dim_date ;;

  # Dimensions

  dimension: date_key {
    description: "Unique integer identifier for a date of the format YYYYMMDD, and primary for the table"
    type: number
    sql: ${TABLE}.date_key ;;
  }

  dimension: calendar_date {
    description: "The calendar date of the form YYYY-MM-DD (e.g. 2020-02-28), also serves as the unique key for this table. Note that 2099-12-31 represents 'multiple dates' and 1970-01-01 represents an unknown or unknown past date"
    type: date
    sql: ${TABLE}.calendar_date ;;
  }

  dimension: day_of_week {
    description: ""
    type: number
    sql: ${TABLE}.day_of_week ;;
  }

  dimension: day_of_week_name {
    description: ""
    type: string
    sql: ${TABLE}.day_of_week_name ;;
  }

  dimension: day_of_month {
    description: ""
    type: number
    sql: ${TABLE}.day_of_month ;;
  }

  dimension: week_of_month {
    description: ""
    type: number
    sql: ${TABLE}.week_of_month ;;
  }

  dimension: calendar_month {
    description: ""
    type: string
    sql: ${TABLE}.calendar_month ;;
  }

  dimension: day_of_quarter {
    description: ""
    type: number
    sql: ${TABLE}.day_of_quarter ;;
  }

  dimension: week_of_quarter {
    description: ""
    type: number
    sql: ${TABLE}.week_of_quarter ;;
  }

  dimension: month_of_quarter {
    description: ""
    type: number
    sql: ${TABLE}.month_of_quarter ;;
  }

  dimension: calendar_quarter {
    description: ""
    type: string
    sql: ${TABLE}.calendar_quarter ;;
  }

  dimension: day_of_year {
    description: ""
    type: number
    sql: ${TABLE}.day_of_year ;;
  }

  dimension: week_of_year {
    description: ""
    type: number
    sql: ${TABLE}.week_of_year ;;
  }

  dimension: month_of_year {
    description: ""
    type: number
    sql: ${TABLE}.month_of_year ;;
  }

  dimension: quarter_of_year {
    description: ""
    type: number
    sql: ${TABLE}.quarter_of_year ;;
  }

  dimension: calendar_year {
    description: ""
    type: number
    sql: ${TABLE}.calendar_year ;;
  }

  dimension: is_leap_year {
    description: "True if the year is part of a leap year, otherwise False"
    type: yesno
    sql: ${TABLE}.is_leap_year ;;
  }

  dimension: is_weekday {
    description: "True if the date is a week day (Mon - Fri), otherwise False"
    type: yesno
    sql: ${TABLE}.is_weekday ;;
  }

  dimension: is_holiday {
    description: "True if the date is a holiday in the United States (based on standard federal holidays), otherwise False"
    type: yesno
    sql: ${TABLE}.is_holiday ;;
  }

  dimension: is_workday {
    description: "True if the date is a working day - a week day and not a holiday, otherwise False"
    type: yesno
    sql: ${TABLE}.is_workday ;;
  }

  dimension: days_in_month {
    description: ""
    type: number
    sql: ${TABLE}.days_in_month ;;
  }

  dimension: days_in_quarter {
    description: ""
    type: number
    sql: ${TABLE}.days_in_quarter ;;
  }

  dimension: days_in_year {
    description: ""
    type: number
    sql: ${TABLE}.days_in_year ;;
  }

  dimension: day_of_week_in_month {
    description: ""
    type: number
    sql: ${TABLE}.day_of_week_in_month ;;
  }

  dimension: day_of_week_in_quarter {
    description: ""
    type: number
    sql: ${TABLE}.day_of_week_in_quarter ;;
  }

  dimension: day_of_week_in_year {
    description: ""
    type: number
    sql: ${TABLE}.day_of_week_in_year ;;
  }

  dimension: first_date_of_week {
    description: ""
    type: date
    sql: ${TABLE}.first_date_of_week ;;
  }

  dimension: last_date_of_week {
    description: ""
    type: date
    sql: ${TABLE}.last_date_of_week ;;
  }

  dimension: first_date_of_month {
    description: ""
    type: date
    sql: ${TABLE}.first_date_of_month ;;
  }

  dimension: last_date_of_month {
    description: ""
    type: date
    sql: ${TABLE}.last_date_of_month ;;
  }

  dimension: first_date_of_quarter {
    description: ""
    type: date
    sql: ${TABLE}.first_date_of_quarter ;;
  }

  dimension: last_date_of_quarter {
    description: ""
    type: date
    sql: ${TABLE}.last_date_of_quarter ;;
  }

  dimension: first_date_of_year {
    description: ""
    type: date
    sql: ${TABLE}.first_date_of_year ;;
  }

  dimension: last_date_of_year {
    description: ""
    type: date
    sql: ${TABLE}.last_date_of_year ;;
  }

  dimension: year_month_day {
    description: ""
    type: number
    sql: ${TABLE}.year_month_day ;;
  }

  dimension: year_month {
    description: ""
    type: number
    sql: ${TABLE}.year_month ;;
  }

  dimension: year_quarter {
    description: ""
    type: number
    sql: ${TABLE}.year_quarter ;;
  }

  dimension: custom_date_detail {
    description: ""
    type: string
    sql: ${TABLE}.custom_date_detail ;;
  }

  dimension_group: row_valid_from_time {
    description: "The timestamp when this version of the row became 'valid', as in it when it began correctly representing reality"
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.row_valid_from_time ;;
  }

  dimension: row_valid_to_time {
    description: "The timestamp when this version of the row was no longer 'valid', as in it when it stopped correctly representing reality"
    type: date
    sql: ${TABLE}.row_valid_to_time ;;
  }

  dimension: is_row_currently_valid {
    description: "True if this version of the record represents the current state of reality"
    type: yesno
    sql: ${TABLE}.is_row_currently_valid ;;
  }

  dimension: scd_unique_key {
    description: "Unique identifier for a version of a row in the base table underlying this dimension table"
    type: string
    sql: ${TABLE}.scd_unique_key ;;
  }

  dimension_group: inserted_at {
    description: "The time when this row was inserted into the table"
    type: time
    timeframes: [
      raw,
      time,
      date,
      week,
      month,
      quarter,
      year
    ]
    sql: ${TABLE}.inserted_at ;;
  }

  # Measures

  measure: count {
    hidden: yes
    type: count
    drill_fields: [detail*]
  }

  # Sets

  set: detail {
    fields: [
      date_key,
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
      year_month_day,
      year_month,
      year_quarter,
      custom_date_detail,
      row_valid_from_time,
      row_valid_to_time,
      is_row_currently_valid,
      scd_unique_key,
      inserted_at
    ]
  }
}

view: another_view {}