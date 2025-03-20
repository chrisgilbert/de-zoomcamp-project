"""
Configuration settings for the data extraction and loading processes.
"""
import os
from dotenv import load_dotenv

# Load environment variables for non-secret configuration
load_dotenv()

# DLT pipeline settings
PIPELINE_NAME = "vehicle_data_pipeline"
DESTINATION = "bigquery"
BQ_DATASET = "vehicle_data"  # Default dataset name, can be overridden in config.toml

# File paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")

# Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)