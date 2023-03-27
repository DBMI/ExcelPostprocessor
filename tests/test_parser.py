"""
Module test_parser.py, which performs automated testing of the ExcelParser class.
"""
from numpy import isnan
import os.path
import pandas
import pytest
from excelpostprocessor.excel_postprocessor import ExcelParser


def test_parser(test_excel_filename):
    #   Test instantiation.
    parser = ExcelParser(excel_filename=test_excel_filename)
    assert isinstance(parser, ExcelParser)

    #   Test extraction to list.
    extracted_data = parser.extract(
        column_name="REPORT", pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})"
    )
    assert isinstance(extracted_data, list)
    assert len(extracted_data) == 3

    #   Test extraction to new dataframe column.
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})",
        new_column="Date",
    )
    df = parser.data()
    assert isinstance(df, pandas.DataFrame)
    assert "Date" in df


def test_parser_corner_cases(test_excel_filename):
    parser = ExcelParser(excel_filename=test_excel_filename, sheet_name="Patients")
    assert isinstance(parser, ExcelParser)

    #   Test extraction to list.
    extracted_data = parser.extract(
        column_name="Empty", pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})"
    )
    assert isinstance(extracted_data, list)
    assert len(extracted_data) == 3
    assert all([isnan(value) for value in extracted_data])


def test_parser_error(test_excel_filename):
    with pytest.raises(TypeError):
        ExcelParser(excel_filename=1979)

    with pytest.raises(FileNotFoundError):
        ExcelParser(excel_filename="not here.excel")

    parser = ExcelParser(excel_filename=test_excel_filename)
    assert isinstance(parser, ExcelParser)

    with pytest.raises(TypeError):
        #   column_name not a str
        parser.extract_into_new_column(
            column_name=1979,
            pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})",
            new_column="Date",
        )

    with pytest.raises(TypeError):
        #   pattern not a str
        parser.extract_into_new_column(
            column_name="REPORT",
            pattern=1979,
            new_column="Date",
        )

    with pytest.raises(AttributeError):
        #   column not present in spreadsheet
        parser.extract_into_new_column(
            column_name="Column Not Here",
            pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})",
            new_column="Date",
        )

    with pytest.raises(ValueError):
        #   pattern contains no capture groups
        parser.extract_into_new_column(
            column_name="REPORT",
            pattern="malformed",
            new_column="Date",
        )

    #   pattern not found
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"not present: (\d+)",
        new_column="Not present",
    )


def test_parser_specified_sheet(test_excel_filename, test_revised_excel_filename):
    #   Test instantiation.
    parser = ExcelParser(excel_filename=test_excel_filename, sheet_name="Labs")
    assert isinstance(parser, ExcelParser)

    #   Test extraction to new dataframe column.
    parser.extract_into_new_column(
        column_name="REPORT", pattern=r"pH: (\d+\.?\d*)", new_column="pH"
    )
    df = parser.data()
    assert isinstance(df, pandas.DataFrame)
    assert "pH" in df

    #   Test writing to default new Excel file.
    new_filename = parser.write_to_excel()
    assert os.path.isfile(new_filename)
    df = pandas.read_excel(new_filename, sheet_name="Labs")
    assert isinstance(df, pandas.DataFrame)
    assert "pH" in df

    #   Test writing to specified new Excel file.
    new_filename = parser.write_to_excel(new_file_name=test_revised_excel_filename)
    assert os.path.isfile(new_filename)
    df = pandas.read_excel(new_filename, sheet_name="Labs")
    assert isinstance(df, pandas.DataFrame)
    assert "pH" in df


def test_parser_writing(test_excel_filename, test_revised_excel_filename):
    #   Test instantiation.
    parser = ExcelParser(excel_filename=test_excel_filename)
    assert isinstance(parser, ExcelParser)

    #   Test extraction of Date to new dataframe column.
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"performed: (\d{1,2}/\d{1,2}/\d{4})",
        new_column="Date",
    )
    df = parser.data()
    assert isinstance(df, pandas.DataFrame)
    assert "Date" in df

    #   Test extraction of temperature.
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"Air temperature: (\d+\.?\d*\s?[^\s\.]+)",
        new_column="Air temp",
    )

    df = parser.data()
    assert isinstance(df, pandas.DataFrame)
    assert "Air temp" in df

    #   Test writing to default new Excel file.
    new_filename = parser.write_to_excel()
    assert os.path.isfile(new_filename)
    df = pandas.read_excel(new_filename)
    assert isinstance(df, pandas.DataFrame)
    assert "Date" in df
    assert "Air temp" in df

    #   Test writing to specified new Excel file.
    new_filename = parser.write_to_excel(new_file_name=test_revised_excel_filename)
    assert os.path.isfile(new_filename)
    df = pandas.read_excel(new_filename)
    assert isinstance(df, pandas.DataFrame)
    assert "Date" in df
    assert "Air temp" in df
