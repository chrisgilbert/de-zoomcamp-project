"""
Tests for the DLT pipeline.
"""
import os
import pytest
from unittest.mock import patch, MagicMock

# Import the modules to test
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dlthub.pipeline import create_pipeline, run_pipeline
from dlthub.extractors.smmt_extractor import SMMTSpider


@pytest.fixture
def mock_secrets():
    """Mock the DLT secrets provider to return test credentials."""
    with patch('dlt.common.configuration.providers.toml.ConfigTomlProvider._read_toml_files') as mock_toml:
        # Create a mock TOML document with test credentials
        mock_toml.return_value = {
            "destination": {
                "bigquery": {
                    "credentials": {
                        "project_id": "test-project",
                        "private_key": "test-key",
                        "client_email": "test@example.com"
                    }
                }
            }
        }
        yield


def test_create_pipeline(mock_secrets):
    """Test creating a DLT pipeline."""
    with patch('dlt.pipeline') as mock_dlt_pipeline:
        mock_pipeline = MagicMock()
        mock_dlt_pipeline.return_value = mock_pipeline
        
        pipeline = create_pipeline()
        
        # Check that dlt.pipeline was called with the correct arguments
        mock_dlt_pipeline.assert_called_once_with(
            pipeline_name="vehicle_data_pipeline",
            destination="bigquery",
            dataset_name="vehicle_data",
            full_refresh=False
        )


def test_run_pipeline():
    """Test running the DLT pipeline."""
    # Create a mock pipeline
    mock_pipeline = MagicMock()
    mock_pipeline.run.return_value = {"load_info": "test"}
    
    # Mock the extractors
    with patch('dlthub.pipeline.smmt_vehicle_data') as mock_smmt, \
         patch('dlthub.pipeline.gov_uk_vehicle_data') as mock_gov_uk:
        
        mock_smmt.return_value = [{
            "fuel": "BEV",
            "monthly_registrations_February_2025": 21244,
            "monthly_registrations_February_2024": 14991,
            "yoy_pct_change": 41.7,
            "market_share_2025": 25.3,
            "market_share_2024": 17.7,
            "data_source": "smmt",
            "extraction_date": "2024-03-19",
            "month": "February"
        }]
        
        mock_gov_uk.return_value = [{
            "region": "Great Britain",
            "year": 2023,
            "quarter": "Q1",
            "vehicle_type": "Cars",
            "fuel_type": "Petrol",
            "count": 12345,
            "data_source": "gov_uk",
            "extraction_date": "2024-03-19"
        }]
        
        # Run the pipeline
        result = run_pipeline(mock_pipeline)
        
        # Check that the pipeline was run with the correct arguments
        assert mock_pipeline.run.call_count == 2
        
        # Check that the result contains the expected keys
        assert "smmt_info" in result
        assert "gov_uk_info" in result


def test_smmt_spider():
    """Test the SMMT spider."""
    # Create a spider instance with a test URL
    test_url = "https://www.smmt.co.uk/vehicle-data/car-registrations/"
    spider = SMMTSpider(start_url=test_url)
    
    # Test that the spider has the correct attributes
    assert hasattr(spider, 'name')
    assert spider.name == 'smmt'
    assert hasattr(spider, 'start_urls')
    assert len(spider.start_urls) > 0
    assert spider.start_urls[0] == test_url 