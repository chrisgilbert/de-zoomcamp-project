"""
Prefect flow for vehicle data pipeline.
"""
from prefect import flow, task
from prefect_dbt.cli.commands import DbtCoreOperation

from dlthub.pipeline import run_pipeline


@task
def extract_and_load_data():
    """Extract and load data using DLT pipeline."""
    return run_pipeline()


@task
def run_dbt_models(command: str = "run"):
    """Run dbt models."""
    dbt_op = DbtCoreOperation(
        commands=[command],
        project_dir="dbt/vehicle_data",
        profiles_dir="dbt/profiles"
    )
    return dbt_op.run()


@flow(name="vehicle_data_pipeline")
def vehicle_data_pipeline(run_tests: bool = False):
    """Main flow for vehicle data pipeline."""
    # Extract and load data
    load_info = extract_and_load_data()
    
    # Run dbt models
    dbt_run = run_dbt_models("run")
    
    # Run tests if requested
    if run_tests:
        dbt_test = run_dbt_models("test")
        return {
            "load_info": load_info,
            "dbt_run": dbt_run,
            "dbt_test": dbt_test
        }
    
    return {
        "load_info": load_info,
        "dbt_run": dbt_run
    }


if __name__ == "__main__":
    # Run the flow directly if this script is executed
    vehicle_data_pipeline() 