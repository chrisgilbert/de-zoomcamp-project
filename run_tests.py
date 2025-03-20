#!/usr/bin/env python
"""
Script to run all tests for the vehicle data project.
"""
import os
import sys
import pytest


def main():
    """Run all tests for the vehicle data project."""
    # Get the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Add the project root to the Python path
    sys.path.insert(0, project_root)
    
    # Run the tests
    exit_code = pytest.main([
        "-v",                  # Verbose output
        "tests/"               # Test directory
    ])
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main()) 