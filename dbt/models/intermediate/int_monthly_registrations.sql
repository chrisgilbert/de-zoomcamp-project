{{ config(materialized="view") }}

with
    gov_uk_data as (
        select
            date_trunc(registration_date, month) as registration_month,
            make,
            fuel_type,
            count(*) as registration_count
        from {{ ref("stg_gov_uk_vehicle_data") }}
        group by 1, 2, 3
    ),

    smmt_data as (
        select
            registration_month,
            'All Makes' as make,
            'All' as fuel_type,
            total_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}

        union all

        select
            registration_month,
            'All Makes' as make,
            'Diesel' as fuel_type,
            diesel_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}

        union all

        select
            registration_month,
            'All Makes' as make,
            'Petrol' as fuel_type,
            petrol_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}

        union all

        select
            registration_month,
            'All Makes' as make,
            'BEV' as fuel_type,
            bev_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}

        union all

        select
            registration_month,
            'All Makes' as make,
            'PHEV' as fuel_type,
            phev_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}

        union all

        select
            registration_month,
            'All Makes' as make,
            'HEV' as fuel_type,
            hev_registrations as registration_count
        from {{ ref("stg_smmt_vehicle_data") }}
    ),

    combined_data as (
        select
            registration_month,
            make,
            fuel_type,
            registration_count,
            'GOV_UK' as data_source
        from gov_uk_data

        union all

        select
            registration_month,
            make,
            fuel_type,
            registration_count,
            'SMMT' as data_source
        from smmt_data
    )

select registration_month, make, fuel_type, registration_count, data_source
from combined_data
