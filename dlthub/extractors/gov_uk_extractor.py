"""
Module for extracting vehicle licensing data from the UK Government website.
"""
import os
import requests
from typing import Dict, List, Optional, Any, Iterator
import pandas as pd
from datetime import datetime
import dlt
from dlthub.config import RAW_DATA_DIR
from prefect import task


# Get configuration from DLT
govuk_config = dlt.config["sources.gov_uk_vehicle_data"]
GB_REGISTRATIONS_URL = govuk_config.get("GB_REGISTRATIONS_URL")
UK_REGISTRATIONS_URL = govuk_config.get("UK_REGISTRATIONS_URL")

@task
def download_file(url: str, filename: str) -> Optional[str]:
    """
    Download a file from a URL and save it to the raw data directory.
    
    Args:
        url: URL of the file to download
        filename: Name to save the file as
        
    Returns:
        Optional[str]: Path to the downloaded file or None if download failed
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        file_path = os.path.join(RAW_DATA_DIR, filename)
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Successfully downloaded {url} to {file_path}")
        return file_path
    except Exception as e:
        print(f"Error downloading file {url}: {e}")
        return None

@task
def process_csv_file(file_path: str) -> Optional[pd.DataFrame]:
    """
    Process a CSV file and extract relevant vehicle data.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        Optional[pd.DataFrame]: DataFrame containing the processed data or None if processing failed
    """
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Basic cleaning and processing
        df.columns = [col.lower().replace(' ', '_') for col in df.columns]
        
        # Add source file information
        if "gb" in file_path.lower():
            df['region'] = 'Great Britain'
            df['data_source'] = 'VEH0160_GB'
        elif "uk" in file_path.lower():
            df['region'] = 'United Kingdom'
            df['data_source'] = 'VEH0160_UK'
        
        # Use string date format for extraction_date
        df['extraction_date'] = datetime.now().date().isoformat()
        
        return df
    except Exception as e:
        print(f"Error processing CSV file {file_path}: {e}")
        return None

@task
@dlt.resource(name="gov_uk_vehicle_data")
def gov_uk_vehicle_data() -> Iterator[Dict[str, Any]]:
    """
    DLT resource for extracting and processing UK Government vehicle data.
    
    Yields:
        Dict[str, Any]: Dictionaries containing processed vehicle data
    """
    # Download and process GB registrations
    gb_file_path = download_file(GB_REGISTRATIONS_URL, "df_VEH0160_GB.csv")
    if gb_file_path:
        gb_df = process_csv_file(gb_file_path)
        if gb_df is not None:
            for record in gb_df.to_dict('records'):
                yield record
    
    # Download and process UK registrations
    uk_file_path = download_file(UK_REGISTRATIONS_URL, "df_VEH0160_UK.csv")
    if uk_file_path:
        uk_df = process_csv_file(uk_file_path)
        if uk_df is not None:
            for record in uk_df.to_dict('records'):
                yield record 