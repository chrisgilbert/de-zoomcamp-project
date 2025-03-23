# Vehicle Registrations Data Engineering Project

## Description

This project extracts data from the UK Government data and SMMT (Society of Motor Manufacturers and Traders).
The SMMT data is not available in free data sets, but the monthly summary data is scraped from their website.

The gov.uk data is available here: https://www.gov.uk/government/statistical-data-sets/vehicle-licensing-statistics-data-files
The latest SMMT data summary is at: https://www.smmt.co.uk/vehicle-data/car-registrations/
At the time of writing it is available up until Sept 2024. 
The SMMT data is then used to supplement the missing months up until Feb 2025.

The project analyzes vehicle registration trends in the UK, focusing on the adoption of different fuel types (petrol, diesel, electric, hybrid) over time.

This helps show the uptake of alternative fuel vehicles. Where available in the gov.uk data, it is broken down into manufactuer, so we can see the most popular brands of EVs and hybrids over time.

## Tech Stack

The supporting infrastructure is:

- Google BigQuery for the data warehouse
- DLT (Data Loading Tool) for ingestion into BigQuery
- DBT (Data Build Tool) for data transformation in BigQuery
- Prefect Cloud for orchestrating the jobs
- Opentofu for managing the underlying infrastructure
- Looker studio for visualizing the data
- SQLFmt for SQL formatting

## Project Structure

```
.
├── dbt/                    # DBT models and configurations
│   ├── models/             # DBT models
│   │   ├── staging/        # Staging models
│   │   ├── intermediate/   # Intermediate models
│   │   └── marts/          # Mart models for analysis
│   ├── dbt_project.yml     # DBT project configuration
│   ├── profiles.yml        # DBT connection profiles
│   └── sqlfmt.toml         # SQL formatting configuration
├── dlt/                    # Data Loading Tool code
│   ├── extractors/         # Data extraction modules
│   │   ├── gov_uk_extractor.py  # UK Government data extractor
│   │   └── smmt_extractor.py    # SMMT data extractor
│   ├── config.py           # Configuration settings
│   └── pipeline.py         # Main pipeline module
├── terraform/              # Terraform (OpenTofu) infrastructure code
├── tests/                  # Test files
│   └── test_dlt_pipeline.py  # Tests for the DLT pipeline
├── data/                   # Data directory (created at runtime)
│   ├── raw/                # Raw data files
│   └── processed/          # Processed data files
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Cloud account with BigQuery enabled
- Google Cloud project already created
- A working gcloud CLI set up with authentication to access it.
- The BigQuery and storage APIs enabled for your CLI user
- Prefect Cloud account (optional, can use local Prefect server)
- Opentofu (for infrastructure setup) 
- Asdf - for managing versions of tools

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vehicle-data-project
   ```

2. Set up environment variables:
   Create a `.env` file with the following variables in the root of the repo:
   ```
   export GCP_PROJECT_ID=your-gcp-project-id
   export BQ_DATASET=vehicle_data
   export GCS_BUCKET=your-gcs-bucket-name
   export PREFECT_API_KEY=your-prefect-api-key
   export PREFECT_WORKSPACE=your-prefect-workspace

3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  
   
   # On Windows: .venv\Scripts\activate
   ```

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Install OpenTofu using the instructions at https://opentofu.org/docs/intro/install/

6. Apply the opentofu configuration:

   ```
   cd tofu
   tofu apply
   ```

7. Check the dlthub secrets file and ensure it is configured correctly:

   cat dlthub/.dlt/secrets.toml

### Running the Pipeline

1. Run the DLT pipeline to extract and load data:
   ```
   cd dlthub
   python -m dlt.pipeline
   ```

3. Run DBT models:
   ```
   cd dbt
   dbt run
   dbt test
   ```

4. Run the Prefect flow (includes DLT pipeline and DBT models):
   ```
   python -m prefect.flows.vehicle_data_flow
   ```

5. Deploy the Prefect flow to Prefect Cloud:
   ```
   python -m prefect.flows.deploy
   ```

## Integration with Prefect and DBT

This project uses prefect-dbt for seamless integration between Prefect and DBT. The Prefect flow:
1. Extracts data using DLT
2. Runs DBT models
3. Runs DBT tests

SQL formatting is handled separately as a development task using the `format_sql.py` script.

The deployment uses Docker infrastructure to ensure consistent execution environments.

## Data Models

### Staging Models
- `stg_gov_uk_vehicle_data`: Standardized vehicle licensing data from the UK Government
- `stg_smmt_vehicle_data`: Standardized vehicle registration data from SMMT

### Intermediate Models
- `int_monthly_registrations`: Combined monthly registration data from both sources

### Mart Models
- `mart_vehicle_registrations`: Analysis of vehicle registrations by fuel type, including market share, year-over-year growth, and rolling totals

## License

[Specify your license here]


