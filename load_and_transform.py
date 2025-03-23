# Run the dlthub pipeline to import data before running the dbt transformations
from prefect import flow, task
from prefect_dbt import PrefectDbtRunner, PrefectDbtSettings

@flow
def run_dlthub_pipeline():
    from dlthub.pipeline import run_pipeline
    run_pipeline()

@flow
def load_and_transform():
    run_dlthub_pipeline()
    run_dbt_transformations()

@flow
def run_dbt_transformations():
    settings = PrefectDbtSettings(project_dir="./dbt", profiles_dir="./dbt")
    runner = PrefectDbtRunner(settings=settings)
    runner.invoke(["build"])

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run data loading and transformation pipeline")
    parser.add_argument("--load-only", action="store_true", help="Only run the data loading step without transformations")
    parser.add_argument("--transform-only", action="store_true", help="Only run the transformation step without loading data")
    args = parser.parse_args()
    
    if args.load_only:
        run_dlthub_pipeline()
    elif args.transform_only:
        run_dbt_transformations()
    else:
        load_and_transform()
