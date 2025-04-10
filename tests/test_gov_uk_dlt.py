"""
Script to test the UK gov car registrations data extractor with dlt integration.
"""

import os
import sys
from pathlib import Path
import dlt

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

# Create data directories if they don't exist
data_dir = Path("data")
raw_dir = data_dir / "raw"
data_dir.mkdir(exist_ok=True)
raw_dir.mkdir(exist_ok=True)

# Import the resource
from dlthub.extractors.gov_uk_extractor import gov_uk_vehicle_data

def test_gov_uk_dlt():
    """
    Test the UK government extractor with dlt integration.
    """
    print("Testing UK government extractor with dlt integration...")
    
    # Create a pipeline
    pipeline = dlt.pipeline(
        pipeline_name="test_gov_uk_pipeline",
        destination="duckdb",
        dataset_name="test_gov_uk_data"
    )
    
    # Run the pipeline with the resource
    info = pipeline.run(
        gov_uk_vehicle_data(),
        write_disposition="replace",
        primary_key=None,
    )
    
    print(f"Loaded {len(info.load_packages)} packages")
    
    if len(info.load_packages) > 0:
        package = info.load_packages[0]
        
        # Print information about the loaded data
        print(f"Load ID: {package.load_id}")
        print(f"State: {package.state}")
        
        # Get completed jobs
        completed_jobs = package.jobs.get('completed_jobs', [])
        if completed_jobs:
            for job in completed_jobs:
                print(f"Loaded table: {job.job_file_info.table_name}")
                print(f"File size: {job.file_size} bytes")
                print(f"Elapsed time: {job.elapsed:.4f} seconds")
        
        # Access the data using a SQL client
        with pipeline.sql_client() as client:
            # Get all tables in the dataset
            tables_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_gov_uk_data'"
            tables = client.query(tables_query).df()
            
            if not tables.empty:
                print(f"Tables in dataset: {', '.join(tables['table_name'].tolist())}")
                
                # Query the first table
                first_table = tables['table_name'].iloc[0]
                print(f"Querying table: {first_table}")
                
                query = f"SELECT * FROM test_gov_uk_data.{first_table} LIMIT 5"
                result = client.query(query).df()
                
                print("First 5 rows:")
                print(result)
            else:
                print("No tables found in the dataset")
    else:
        print("No data was loaded")

if __name__ == "__main__":
    test_gov_uk_dlt() 