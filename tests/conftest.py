"""
Contains test fixtures available across all test_*.py files.
"""
import os
import pytest


@pytest.fixture(name="test_config_filename")
def fixture_test_config_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "excel_postprocessor.xml")


@pytest.fixture(name="test_config_filename_multiple_rules")
def fixture_test_config_filename_multiple_rules() -> str:
    return os.path.join(
        os.path.dirname(__file__), "excel_postprocessor_multiple_rules.xml"
    )


@pytest.fixture(name="test_excel_filename")
def fixture_test_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "dummy_data.xlsx")


@pytest.fixture(name="test_labs_excel_filename")
def fixture_test_labs_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "test_data_Labs.xlsx")


@pytest.fixture(name="test_malformed_config_filename")
def fixture_test_malformed_config_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "malformed.xml")


@pytest.fixture(name="test_patients_excel_filename")
def fixture_test_patients_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "test_data_Patients.xlsx")


@pytest.fixture(name="test_realistic_excel_filename")
def fixture_test_realistic_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "test_data.xlsx")


@pytest.fixture(name="test_revised_excel_filename")
def fixture_test_revised_excel_filename() -> str:
    return os.path.join(os.path.dirname(__file__), "revised_dummy_data.xlsx")
