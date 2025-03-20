"""
Script to test the Scrapy spider for the SMMT website using dlt integration.
"""
import os
import sys
import argparse
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
from dlthub.extractors.smmt_extractor import smmt_vehicle_data

def test_smmt_spider(query_only=False):
    """
    Test the SMMT spider with dlt integration.
    
    Args:
        query_only: If True, only query the existing data without running the spider
    """
    print("Testing SMMT spider with dlt integration...")
    
    # Create a pipeline using the configuration from .dlt/config.toml
    pipeline = dlt.pipeline(
        pipeline_name="test_smmt_pipeline",
        destination="duckdb",
        dataset_name="test_smmt_data"
    )
    
    # Run the pipeline with the resource if not query_only
    if not query_only:
        print("Running the SMMT spider...")
        info = pipeline.run(
            smmt_vehicle_data(),  # No need to specify save_html, it will use the config value
            write_disposition="replace",  # Replace existing data
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
        else:
            print("No data was loaded")
    else:
        print("Skipping spider run, querying existing data only...")
    
    # Access the data using a SQL client
    with pipeline.sql_client() as client:
        # Get all tables in the dataset
        tables_query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = 'test_smmt_data'"
        tables = client.query(tables_query).df()
        
        if not tables.empty:
            print(f"Tables in dataset: {', '.join(tables['table_name'].tolist())}")
            
            # Query the first table
            first_table = tables['table_name'].iloc[0]
            print(f"Querying table: {first_table}")
            
            # Select specific columns with proper names
            query = f"""
            SELECT 
                fuel, 
                monthly_registrations_February_2025,
                monthly_registrations_February_2024,
                yoy_pct_change,
                market_share_2025,
                market_share_2024,
                data_source,
                extraction_date,
                month
            FROM test_smmt_data.{first_table} 
            LIMIT 5
            """
            result = client.query(query).df()
            
            print("First 5 rows:")
            print(result)
        else:
            print("No tables found in the dataset")

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Test the SMMT spider with dlt integration.')
    parser.add_argument('--query-only', action='store_true', 
                        help='Only query the existing data without running the spider')
    args = parser.parse_args()
    
    # Run the test with the provided arguments
    test_smmt_spider(query_only=args.query_only) 