"""
Contains test fixtures available across all test_*.py files.
"""
import os
import pytest


@pytest.fixture(name="test_excel_filename")
def fixture_test_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "dummy_data.xlsx")


@pytest.fixture(name="test_revised_excel_filename")
def fixture_test_revised_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "revised_dummy_data.xlsx")
