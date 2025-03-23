"""
Main pipeline module for loading vehicle data into BigQuery.
"""
import dlt
from typing import Dict, Any, Optional

from dlthub.config import PIPELINE_NAME, DESTINATION, BQ_DATASET
from dlthub.extractors import gov_uk_vehicle_data
from prefect import flow, task

@task
def create_pipeline() -> dlt.Pipeline:
    """
    Create a DLT pipeline for loading vehicle data.
    """
    # Configure pipeline
    # Credentials will be loaded automatically from .dlt/secrets.toml
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination=DESTINATION,
        dataset_name=BQ_DATASET,
        full_refresh=False,
    )
    return pipeline

@flow
def run_pipeline(pipeline: Optional[dlt.Pipeline] = None) -> Dict[str, Any]:
    if pipeline is None:
        pipeline = create_pipeline()
    
    # Load UK Government vehicle data
    @task
    def run_load_data():
        return pipeline.run(
            gov_uk_vehicle_data(), 
            table_name="gov_uk_vehicle_data",
            write_disposition="replace"
        )
        
    gov_uk_info = run_load_data()
    
    return {
        "gov_uk_info": gov_uk_info
    }

if __name__ == "__main__":
    # Run the pipeline directly if this script is executed
    pipeline_info = run_pipeline()
    print(f"Pipeline run complete: {pipeline_info}") 
    run_pipeline.serve("run_pipeline", cron="0 0 * * *")
