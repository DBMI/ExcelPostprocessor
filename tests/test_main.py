"""
Module test_main.py, which performs automated testing of the ParserRunner class.
"""
import os
import pandas
import pytest
from excelpostprocessor.parser_runner import ParserRunner


def test_cfg_file(test_config_filename, test_patients_excel_filename):
    if os.path.exists(test_patients_excel_filename):
        os.remove(test_patients_excel_filename)

    assert not os.path.exists(test_patients_excel_filename)

    runner = ParserRunner(config_filename=test_config_filename)
    runner.process()

    assert os.path.exists(test_patients_excel_filename)

    #   Check that the created Excel file 'REPORT' column still contains the original error.
    #   We cleaned the column to extract data, but want to retain the original text.
    df = pandas.read_excel(test_patients_excel_filename, sheet_name="Patients")
    assert isinstance(df, pandas.DataFrame)
    assert "VL EF MOD" in df.iloc[3]["REPORT"]


def test_cleaning(
    test_config_filename_single_cleaning_rule, test_patients_excel_filename
):
    if os.path.exists(test_patients_excel_filename):
        os.remove(test_patients_excel_filename)

    assert not os.path.exists(test_patients_excel_filename)

    runner = ParserRunner(config_filename=test_config_filename_single_cleaning_rule)
    runner.process()

    assert os.path.exists(test_patients_excel_filename)

    #   Check that the created Excel file 'REPORT' column still contains the original error.
    #   We cleaned the column to extract data, but want to retain the original text.
    df = pandas.read_excel(test_patients_excel_filename, sheet_name="Patients")
    assert isinstance(df, pandas.DataFrame)
    assert "VL EF MOD" in df.iloc[3]["REPORT"]


def test_error_cases(
    test_config_filename_cleaning_pattern_missing,
    test_config_filename_cleaning_replace_missing,
    test_config_filename_column_dict_missing,
    test_config_filename_column_name_field_missing,
    test_config_filename_column_name_missing,
    test_malformed_config_filename,
    test_config_filename_extract_missing,
    test_config_filename_extract_pattern_missing,
    test_config_filename_extract_new_column_missing,
    test_config_filename_sheet_dict_missing,
    test_config_filename_sheet_name_missing,
    test_config_filename_sheet_name_field_missing,
    test_config_filename_source_column_field_missing,
    test_config_filename_workbook_dict_missing,
    test_config_filename_workbook_field_missing,
    test_config_filename_workbook_name_missing,
    test_config_filename_workbook_name_field_missing,
    test_config_filename_workbook_name_not_found,
):
    with pytest.raises(TypeError):
        ParserRunner(config_filename=1979)

    with pytest.raises(FileExistsError):
        ParserRunner(config_filename="not there.xml")

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_cleaning_pattern_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_cleaning_replace_missing
        )
        parser.process()

    with pytest.raises(TypeError):
        parser = ParserRunner(config_filename=test_config_filename_column_dict_missing)
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_column_name_field_missing
        )
        parser.process()

    with pytest.raises(TypeError):
        parser = ParserRunner(config_filename=test_config_filename_column_name_missing)
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(config_filename=test_malformed_config_filename)
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(config_filename=test_config_filename_extract_missing)
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_extract_pattern_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_extract_new_column_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(config_filename=test_config_filename_sheet_dict_missing)
        parser.process()

    with pytest.raises(TypeError):
        parser = ParserRunner(config_filename=test_config_filename_sheet_name_missing)
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_sheet_name_field_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_source_column_field_missing
        )
        parser.process()

    with pytest.raises(TypeError):
        parser = ParserRunner(
            config_filename=test_config_filename_workbook_dict_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_workbook_field_missing
        )
        parser.process()

    with pytest.raises(FileExistsError):
        parser = ParserRunner(
            config_filename=test_config_filename_workbook_name_missing
        )
        parser.process()

    with pytest.raises(SyntaxError):
        parser = ParserRunner(
            config_filename=test_config_filename_workbook_name_field_missing
        )
        parser.process()

    with pytest.raises(FileExistsError):
        parser = ParserRunner(
            config_filename=test_config_filename_workbook_name_not_found
        )
        parser.process()


def test_main(test_config_filename_ivus):
    parser = ParserRunner(config_filename=test_config_filename_ivus)
    parser.process()


def test_multiple_rules(test_config_filename_multiple_rules, test_labs_excel_filename):
    if os.path.exists(test_labs_excel_filename):
        os.remove(test_labs_excel_filename)

    assert not os.path.exists(test_labs_excel_filename)

    runner = ParserRunner(config_filename=test_config_filename_multiple_rules)
    runner.process()

    assert os.path.exists(test_labs_excel_filename)

    #   Check that we correctly parsed the pH info out of the source spreadsheet,
    #   even though the number and 'pH' tags are in reverse order on one line.
    df = pandas.read_excel(test_labs_excel_filename, sheet_name="Labs")
    assert isinstance(df, pandas.DataFrame)
    assert df.iloc[3]["pH"] == 10.83


def test_sheet_missing(test_config_filename_sheet_missing):
    runner = ParserRunner(config_filename=test_config_filename_sheet_missing)
    assert not runner.process()
