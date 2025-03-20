{{ config(materialized="table") }}

with
    monthly_data as (
        select registration_month, make, fuel_type, registration_count, data_source
        from {{ ref("int_monthly_registrations") }}
    ),

    -- Calculate market share by fuel type for each month
    market_share as (
        select
            registration_month,
            fuel_type,
            sum(registration_count) as fuel_type_count,
            sum(sum(registration_count)) over (
                partition by registration_month
            ) as total_month_count,
            safe_divide(
                sum(registration_count),
                sum(sum(registration_count)) over (partition by registration_month)
            ) as market_share
        from monthly_data
        where fuel_type != 'All'  -- Exclude the 'All' category to avoid double counting
        group by 1, 2
    ),

    -- Calculate year-over-year growth
    yoy_growth as (
        select
            current_month.registration_month,
            current_month.fuel_type,
            current_month.fuel_type_count,
            prev_year.fuel_type_count as prev_year_count,
            safe_divide(
                current_month.fuel_type_count - prev_year.fuel_type_count,
                prev_year.fuel_type_count
            ) as yoy_growth
        from market_share current_month
        left join
            market_share prev_year
            on current_month.fuel_type = prev_year.fuel_type
            and date_sub(current_month.registration_month, interval 1 year)
            = prev_year.registration_month
    ),

    -- Calculate rolling 12-month totals
    rolling_totals as (
        select
            registration_month,
            fuel_type,
            fuel_type_count,
            sum(fuel_type_count) over (
                partition by fuel_type
                order by
                    registration_month
                    range between interval 11 month preceding and current row
            ) as rolling_12_month_total
        from market_share
    )

select
    r.registration_month,
    r.fuel_type,
    r.fuel_type_count as monthly_registrations,
    m.market_share,
    y.yoy_growth,
    r.rolling_12_month_total,
    extract(year from r.registration_month) as registration_year,
    extract(month from r.registration_month) as registration_month_num,
    format_date('%b', r.registration_month) as registration_month_name,
    case
        when r.fuel_type in ('BEV', 'PHEV', 'HEV')
        then 'Electric/Hybrid'
        else 'Conventional'
    end as powertrain_category
from rolling_totals r
join
    market_share m
    on r.registration_month = m.registration_month
    and r.fuel_type = m.fuel_type
left join
    yoy_growth y
    on r.registration_month = y.registration_month
    and r.fuel_type = y.fuel_type
order by r.registration_month desc, r.fuel_type
