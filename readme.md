# Vehicle Registrations Data Engineering Project

## Description

This project analyzes vehicle registration trends in the UK, focusing on the adoption of different fuel types (petrol, diesel, electric, hybrid) over time.

The project extracts data from the uk.gov car registrations data sets.

The gov.uk data is available here: https://www.gov.uk/government/statistical-data-sets/vehicle-licensing-statistics-data-files

This helps show the uptake of alternative fuel vehicles. The data is loaded and then transformed to add useful reporting aggregations so we can see the fuel type adoption over time, and the different fuel types by vehicle manufacturer.

## Tech Stack

The supporting infrastructure and tooling is:

- Google BigQuery for the data warehouse
- DLT (Data Loading Tool) for copying to GCP storage and then ingestion into BigQuery
- DBT (Data Build Tool) for data transformations in BigQuery
- Prefect Cloud for orchestrating the load and transformation jobs
- Opentofu for managing the underlying infrastructure
- Looker studio for visualizing the data
- Make for simplfying the local command runs and setup

## Project Structure

```
.
├── dbt/                      # DBT models and configurations
│   ├── models/               # DBT models
│   │   ├── staging/          # Staging models
│   │   └── reporting/        # Reporting models for analysis
│   ├── dbt_project.yml       # DBT project configuration
│   ├── profiles.yml          # DBT connection profiles
│   └── sqlfmt.toml           # SQL formatting configuration
├── dlthub/                   # Data Loading Tool code
│   ├── extractors/           # Data extraction modules
│   │   ├── gov_uk_extractor.py  # UK Government data extractor
│   ├── config.py             # Configuration settings
│   └── pipeline.py           # Main pipeline module
├── opentofu/                 # OpenTofu (terraform) infrastructure code
├── tests/                    # Test files
│   └── test_dlt_pipeline.py  # Tests for the DLT pipeline
├── dlthub/data               # Temporary data directory (created at runtime)
│   ├── raw/                  # Raw data files
│   └── processed/            # Processed data files
├── requirements.txt          # Python dependencies
└── readme.md                 # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Google Cloud account with BigQuery and storage enabled
- Google Cloud project already created
- A working gcloud CLI set up with authentication to access it.
- The BigQuery and storage APIs enabled for your CLI user
- Opentofu (for infrastructure setup) 

There is some assistance and documentation on setting these up below. 

Before you begin, please create a project in Google BigQuery if you don't already have an appropriate one to use.

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd vehicle-data-project
   ```

2. Set up environment variables:
   Create a `.env` file with the following variables in the root of the repo
   
   ```
   cp .env.example .env
   ```
   Change the file to ensure the following env vars are set at the top of the file 
   (you do not need to change the rest of the file)

   ```
   export GCP_PROJECT_ID=your-gcp-project-id
   export GCS_BUCKET=your-gcs-bucket-name
   ```

3. Create and activate a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  
   
   # On Windows: .venv\Scripts\activate
   ```

4. Ensure you have a gcloud cli installed, following the setup instructions here:
   https://cloud.google.com/sdk/docs/install 

   Setup the default authentication profile by running the following command, and logging in with your browser:
   ```
   gcloud auth application-default login 
   ```

5. Run the python setup script using make. This should install the dependencies, and 
   setup a local instance of prefect server.
   ```
   make setup
   ```

6. Install OpenTofu using the instructions at https://opentofu.org/docs/intro/install/

7. Apply the opentofu configuration to create the cloud infrastructure in GCP:

   ```
   make tofu
   ```

### Running the Pipeline

1. Run the DLT pipeline to download and load data:
   ```
   make load
   ```

3. Run DBT transformations:
   ```
   make transformations
   ```

If this all works, you will have a vehicle_data dataset with some tables and views beneath it in BigQuery.

## Data Models

### Staging Models
- `stg_gov_uk_vehicle_data`: Standardized vehicle licensing data from the UK Government

### Reporting Models
- `rep_aggregations_by_manufacturer`: Analysis of registrations by vehicle manufacturer
- `rep_aggregations_by_fuel_type`: Breakdown of registrations by fuel type

## License

MIT


