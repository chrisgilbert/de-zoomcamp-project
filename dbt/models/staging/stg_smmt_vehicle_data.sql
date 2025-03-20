{{ config(materialized="view") }}

with
    source_data as (select * from {{ source("raw", "smmt_vehicle_data") }}),

    renamed as (
        select
            -- Adjust these column names based on the actual data structure
            -- This is a placeholder that you'll need to update
            cast(month as date) as registration_month,
            cast(total_registrations as int64) as total_registrations,
            cast(private_registrations as int64) as private_registrations,
            cast(fleet_registrations as int64) as fleet_registrations,
            cast(business_registrations as int64) as business_registrations,
            cast(diesel_registrations as int64) as diesel_registrations,
            cast(petrol_registrations as int64) as petrol_registrations,
            cast(bev_registrations as int64) as bev_registrations,
            cast(phev_registrations as int64) as phev_registrations,
            cast(hev_registrations as int64) as hev_registrations,

            -- Metadata
            cast(data_source as string) as data_source,
            cast(extraction_date as date) as extraction_date
        from source_data
    )

select *
from renamed
