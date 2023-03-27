"""
Module test_main.py, which performs automated testing of the ParserRunner class.
"""
import os
import pytest
from excelpostprocessor.parser_runner import ParserRunner


def test_cfg_file(test_config_filename, test_patients_excel_filename):
    if os.path.exists(test_patients_excel_filename):
        os.remove(test_patients_excel_filename)

    assert not os.path.exists(test_patients_excel_filename)

    runner = ParserRunner(config_filename=test_config_filename)
    runner.run()

    assert os.path.exists(test_patients_excel_filename)


def test_error_cases(test_malformed_config_filename):
    with pytest.raises(TypeError):
        ParserRunner(config_filename=1979)

    with pytest.raises(FileExistsError):
        ParserRunner(config_filename="not there.xml")

    with pytest.raises(SyntaxError):
        parser = ParserRunner(config_filename=test_malformed_config_filename)
        parser.run()
