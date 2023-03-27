import os
from excelpostprocessor.excel_postprocessor import ExcelParser


def test_more_realistic(test_realistic_excel_filename, test_patients_excel_filename):
    parser = ExcelParser(
        excel_filename=test_realistic_excel_filename, sheet_name="Patients"
    )

    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"Date of Exam:\s?(\d{1,2}/\d{1,2}/\d{4})",
        new_column="Date of Exam",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"LV EF MOD BP:\s?(\d+\.?\d*\s?%)",
        new_column="LV EF %",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"LVIDd:\s?(\d+\.?\d*\s?cm)",
        new_column="LVIDd",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"RVSP/PASP:\s?(\d+\.?\d*\s?mmHg)",
        new_column="RVSP",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"TAPSE \(2D\):\s?(\d+\.?\d*\s?cm)",
        new_column="TAPSE (2D)",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"RV S. Vmax:\s?(\d+\.?\d*\s?m/s)",
        new_column="RV S' Vmax",
    )
    parser.extract_into_new_column(
        column_name="REPORT",
        pattern=r"MV e. \(lateral\):\s?(\d+\.?\d*\s?m/s)",
        new_column="MV e' lateral",
    )

    if os.path.exists(test_patients_excel_filename):
        os.remove(test_patients_excel_filename)

    assert not os.path.exists(test_patients_excel_filename)
    parser.write_to_excel(new_file_name=test_patients_excel_filename)
    assert os.path.exists(test_patients_excel_filename)
