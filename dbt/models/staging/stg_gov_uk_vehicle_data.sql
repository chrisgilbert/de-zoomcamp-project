{{ config(materialized="view") }}

with
    source_data as (select * from {{ source("raw", "gov_uk_vehicle_data") }}),

    renamed as (
        select
            -- These columns are based on the VEH0160 dataset structure
            cast(year_month as date) as registration_date,
            cast(body_type as string) as body_type,
            cast(fuel_type as string) as fuel_type,
            cast(number_of_vehicles as int64) as registration_count,

            -- Metadata added by our extractor
            cast(region as string) as region,
            cast(data_source as string) as data_source,
            cast(extraction_date as date) as extraction_date
        from source_data
    )

select *
from renamed
