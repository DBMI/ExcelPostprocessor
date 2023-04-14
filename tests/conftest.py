"""
Contains test fixtures available across all test_*.py files.
"""
import os
import pytest


@pytest.fixture(name="test_config_filename")
def fixture_test_config_filename(request) -> str:
    # https://medium.com/opsops/how-to-get-directory-with-test-from-fixture-in-conftest-py-275b566fcc00
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor.xml")


@pytest.fixture(name="test_config_filename_cleaning_pattern_missing")
def fixture_test_config_filename_cleaning_pattern_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_cleaning_pattern_missing.xml")


@pytest.fixture(name="test_config_filename_cleaning_replace_missing")
def fixture_test_config_filename_cleaning_replace_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_cleaning_replace_missing.xml")


@pytest.fixture(name="test_config_filename_column_dict_missing")
def fixture_test_config_filename_column_dict_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_column_dict_missing.xml")


@pytest.fixture(name="test_config_filename_column_name_field_missing")
def fixture_test_config_filename_column_name_field_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_column_name_field_missing.xml")


@pytest.fixture(name="test_config_filename_column_name_missing")
def fixture_test_config_filename_column_name_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_column_name_missing.xml")


@pytest.fixture(name="test_config_filename_extract_pattern_missing")
def fixture_test_config_filename_extract_pattern_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_extract_pattern_missing.xml")


@pytest.fixture(name="test_config_filename_extract_new_column_missing")
def fixture_test_config_filename_extract_new_column_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_extract_new_column_missing.xml")


@pytest.fixture(name="test_config_filename_extract_missing")
def fixture_test_config_filename_extract_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_extract_missing.xml")


@pytest.fixture(name="test_config_filename_ivus")
def fixture_test_config_filename_ivus(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_ivus.xml")


@pytest.fixture(name="test_config_filename_multiple_rules")
def fixture_test_config_filename_multiple_rules(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_multiple_rules.xml")


@pytest.fixture(name="test_config_filename_sheet_dict_missing")
def fixture_test_config_filename_sheet_dict_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_sheet_dict_missing.xml")


@pytest.fixture(name="test_config_filename_sheet_missing")
def fixture_test_config_filename_sheet_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_sheet_missing.xml")


@pytest.fixture(name="test_config_filename_sheet_name_missing")
def fixture_test_config_filename_sheet_name_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_sheet_name_missing.xml")


@pytest.fixture(name="test_config_filename_sheet_name_field_missing")
def fixture_test_config_filename_sheet_name_field_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_sheet_name_field_missing.xml")


@pytest.fixture(name="test_config_filename_single_cleaning_rule")
def fixture_test_config_filename_sheet_single_cleaning_rule(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_single_cleaning_rule.xml")


@pytest.fixture(name="test_config_filename_source_column_field_missing")
def fixture_test_config_filename_source_column_field_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_source_column_field_missing.xml")


@pytest.fixture(name="test_config_filename_workbook_dict_missing")
def fixture_test_config_filename_workbook_dict_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_workbook_dict_missing.xml")


@pytest.fixture(name="test_config_filename_workbook_field_missing")
def fixture_test_config_filename_workbook_field_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_workbook_field_missing.xml")


@pytest.fixture(name="test_config_filename_workbook_name_field_missing")
def fixture_test_config_filename_workbook_name_field_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_workbook_name_field_missing.xml")


@pytest.fixture(name="test_config_filename_workbook_name_missing")
def fixture_test_config_filename_workbook_name_missing(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_workbook_name_missing.xml")


@pytest.fixture(name="test_config_filename_workbook_name_not_found")
def fixture_test_config_filename_workbook_name_not_found(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "excel_postprocessor_workbook_name_not_found.xml")


@pytest.fixture(name="test_excel_filename")
def fixture_test_excel_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "dummy_data.xlsx")


@pytest.fixture(name="test_labs_excel_filename")
def fixture_test_labs_excel_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "test_data_Labs.xlsx")


@pytest.fixture(name="test_malformed_config_filename")
def fixture_test_malformed_config_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "malformed.xml")


@pytest.fixture(name="test_patients_excel_filename")
def fixture_test_patients_excel_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "test_data_Patients.xlsx")


@pytest.fixture(name="test_realistic_excel_filename")
def fixture_test_realistic_excel_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "test_data.xlsx")


@pytest.fixture(name="test_revised_excel_filename")
def fixture_test_revised_excel_filename(request) -> str:
    test_dir = os.path.dirname(request.module.__file__)
    return os.path.join(test_dir, "revised_dummy_data.xlsx")
