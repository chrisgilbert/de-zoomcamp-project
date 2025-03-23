{% set fuels = {
        'Diesel': 'Diesel',
        'Petrol': 'Petrol',
        'Battery electric': 'Battery EV',
        'Plug-in hybrid electric%': 'Plug-in Hybrid EV',
        'Hybrid electric%': 'Hybrid EV',
        'Fuel cell%': 'Fuel Cell EV',
        'Other fuel types': 'Other',
        'Gas': 'LPG',
    } 
%}

with normalised_fuel_types as (
select 
    registrations,
    year,
    quarter_number,
    make, 
    model, 
    genmodel, 
    bodytype,
    region,
    case
    {%- for fuel in fuels.keys() %}
        when fuel like '{{ fuel }}' then '{{ fuels[fuel] }}'
    {% endfor %}
    else 'Other'
    end as fuel_type_normalised
from {{ ref('stg_unpivot_gov_uk_vehicles') }}
),

summary as (
    select 
        sum(registrations) as registrations,
        year,
        quarter_number,
        make, 
        model, 
        genmodel, 
        bodytype,
        region,
        fuel_type_normalised
    from normalised_fuel_types
    group by 2, 3, 4, 5, 6, 7, 8, 9
)

select * from summary

