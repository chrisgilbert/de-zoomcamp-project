select
    year,
    quarter_number,
    make,
    fuel_type_normalised,
    sum(registrations) as registrations
from {{ ref('stg_normalised_fuel_types_gov_uk') }}
group by year, quarter_number, make, fuel_type_normalised
order by year desc, quarter_number asc, make asc, fuel_type_normalised asc