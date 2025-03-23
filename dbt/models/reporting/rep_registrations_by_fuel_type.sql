select
    year,
    quarter_number,
    fuel,
    sum(registrations) as registrations
from {{ ref('stg_unpivot_gov_uk_vehicles') }}
group by year, quarter_number, fuel
order by year desc, quarter_number asc