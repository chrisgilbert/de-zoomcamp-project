"""
Simple script to test the UK government extractor directly.
"""
import os
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Create data directories if they don't exist
data_dir = os.path.join(project_root, "data")
raw_data_dir = os.path.join(data_dir, "raw")
os.makedirs(raw_data_dir, exist_ok=True)

# Import the extractor
from dlthub.extractors.gov_uk_extractor import (
    download_file,
    process_csv_file
)

# Load environment variables from .env file
load_dotenv()

# Get URLs from environment variables
GB_REGISTRATIONS_URL = os.getenv("GB_REGISTRATIONS_URL", "https://assets.publishing.service.gov.uk/media/66f15d48bd3aced9da489bdf/df_VEH0160_GB.csv")
UK_REGISTRATIONS_URL = os.getenv("UK_REGISTRATIONS_URL", "https://assets.publishing.service.gov.uk/media/66f15d6a7aeb85342827abdc/df_VEH0160_UK.csv")


def test_download_and_process():
    """Test downloading and processing the UK government data."""
    print("Testing UK government extractor...")
    
    # Download and process GB registrations
    print(f"Downloading GB registrations from {GB_REGISTRATIONS_URL}")
    gb_file_path = download_file(GB_REGISTRATIONS_URL, "df_VEH0160_GB.csv")
    if gb_file_path:
        print(f"Successfully downloaded GB registrations to {gb_file_path}")
        gb_df = process_csv_file(gb_file_path)
        if gb_df is not None:
            print(f"Successfully processed GB registrations. Shape: {gb_df.shape}")
            print("First few rows:")
            print(gb_df.head())
        else:
            print("Failed to process GB registrations")
    else:
        print("Failed to download GB registrations")
    
    # Download and process UK registrations
    print(f"\nDownloading UK registrations from {UK_REGISTRATIONS_URL}")
    uk_file_path = download_file(UK_REGISTRATIONS_URL, "df_VEH0160_UK.csv")
    if uk_file_path:
        print(f"Successfully downloaded UK registrations to {uk_file_path}")
        uk_df = process_csv_file(uk_file_path)
        if uk_df is not None:
            print(f"Successfully processed UK registrations. Shape: {uk_df.shape}")
            print("First few rows:")
            print(uk_df.head())
        else:
            print("Failed to process UK registrations")
    else:
        print("Failed to download UK registrations")

if __name__ == "__main__":
    test_download_and_process() 