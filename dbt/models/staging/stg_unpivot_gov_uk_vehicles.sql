-- unpivot the gov uk vehicle data to get a row for each quarter instead of many columns
-- partition by year and cluster by fuel to improve query performance
{{ 
    config(
        materialized='table',
        partition_by={
            "field": "year",
            "data_type": "int",
            "range": {
                "start": 1980,
                "end": 2050,
                "interval": 1
            }
        },
        cluster_by = "fuel"
    )
}}

{% set quarter_pattern = '^_\\d{4}q[1-4]$' %}
{% set quarters = [] %}
{% for col in adapter.get_columns_in_relation(source('raw', 'gov_uk_vehicle_data')) %}
    {% if modules.re.match(quarter_pattern, col.name) %}
        {% do quarters.append(col.name) %}
    {% endif %}
{% endfor %}

select 
    registrations, 
    quarter, 
    cast(regexp_extract(quarter, '_(\\d{4})q.*', 1) as int) as year,
    cast(regexp_extract(quarter, '.*q(\\d)', 2) as int) as quarter_number,
    fuel, 
    make, 
    model, 
    genmodel, 
    bodytype,
    region
from {{ source("raw", "gov_uk_vehicle_data") }}
unpivot(
    registrations for quarter in (
        {{ quarters | join(', ') }}
    )
)



