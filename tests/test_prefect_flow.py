"""
Tests for the Prefect flow.
"""
import os
import pytest
from unittest.mock import patch, MagicMock

# Import the modules to test
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock the prefect_dbt module
sys.modules['prefect_dbt'] = MagicMock()
sys.modules['prefect_dbt.cli'] = MagicMock()
sys.modules['prefect_dbt.cli.commands'] = MagicMock()
sys.modules['prefect_dbt.cli.commands'].DbtCoreOperation = MagicMock

# Use the new workflows directory instead of prefect
from workflows.flows.vehicle_data_flow import (
    extract_and_load_data,
    run_dbt_models,
    vehicle_data_pipeline
)


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


def test_extract_and_load_data(mock_secrets):
    """Test the extract_and_load_data task."""
    # Skip the actual DLT pipeline execution by patching the run_pipeline function
    with patch('workflows.flows.vehicle_data_flow.run_pipeline') as mock_run_pipeline:
        # Set up the mock return value
        mock_run_pipeline.return_value = {"test": "data"}
        
        # Call the function
        result = extract_and_load_data.fn()  # Call the function directly, not the task
        
        # Check that run_pipeline was called
        mock_run_pipeline.assert_called_once()
        assert result == {"test": "data"}


def test_run_dbt_models():
    """Test the run_dbt_models task."""
    # Use patch to mock the DbtCoreOperation class
    with patch('workflows.flows.vehicle_data_flow.DbtCoreOperation') as mock_dbt_op_class:
        # Set up the mock
        mock_instance = MagicMock()
        mock_instance.run.return_value = MagicMock(success=True)
        mock_dbt_op_class.return_value = mock_instance
        
        # Call the function directly, not the task
        result = run_dbt_models.fn("run")
        
        # Check that DbtCoreOperation was called with the correct arguments
        mock_dbt_op_class.assert_called_once()
        assert "run" in mock_dbt_op_class.call_args[1]['commands']
        
        # Check that run was called on the instance
        mock_instance.run.assert_called_once()


def test_vehicle_data_pipeline(mock_secrets):
    """Test the vehicle_data_pipeline flow."""
    # Use the correct module path for patching
    with patch('workflows.flows.vehicle_data_flow.extract_and_load_data') as mock_extract, \
         patch('workflows.flows.vehicle_data_flow.run_dbt_models') as mock_run_dbt:
        
        # Set up the mocks
        mock_extract.return_value = {"test": "data"}
        
        # Call the flow
        vehicle_data_pipeline(run_tests=True)
        
        # Check that all tasks were called
        mock_extract.assert_called_once()
        assert mock_run_dbt.call_count == 2  # Once for run, once for test 