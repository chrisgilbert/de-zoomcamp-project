"""
Test module for SMMT data extraction.
"""
from dlthub.extractors.smmt_extractor import smmt_vehicle_data

if __name__ == "__main__":
    # Run the SMMT extractor
    for item in smmt_vehicle_data():
        print(item) 