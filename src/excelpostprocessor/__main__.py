"""
    Excel Postprocessor applies Regular Expressions to an existing Excel workbook, extracting data into a new column.
"""
import argparse
import sys
from typing import Union

from excelpostprocessor.parser_runner import ParserRunner

CONFIG_FILENAME = "excel_postprocessor.xml"


def main(config_filename: Union[str, None] = None) -> None:
    runner = ParserRunner(config_filename=config_filename)
    runner.process()


if __name__ == "__main__":
    #   Handle 'help' case.
    parser = argparse.ArgumentParser(
        description=r"""
        Excel Postprocessor applies Regular Expressions to an existing Excel workbook, extracting data
        into a new column. You must provide an XML configuration file that lists:

        1) Name of the Excel workbook to process
        2) Sheet(s) to be processed
        3) The Regular Expression to use and the new column to be created. Here's an example file:

        <workbook>
            <name>test_data.xlsx</name>
            <sheet>
                <name>Patients</name>
                <source_column>
                    <name>Report</name>
                    <extract>
                        <pattern>Date of Exam:\s?(\d{1,2}/\d{1,2}/\d{4})</pattern>
                        <new_column>Date of Exam</new_column>
                    </extract>
                    <extract>
                        <pattern>LV EF MOD BP:\s?(\d+\.?\d*\s?)%</pattern>
                        <new_column>LV EF %</new_column>
                    </extract>
                </source_column>
            </sheet>
        </workbook>

        Run the app with:
            excel_postprocess.exe --config <name of config file.xml>

        If the config file name is not specified, app will look for the default file excel_postprocessor.xml.
        """,
        epilog="""The app creates a new Excel workbook for each worksheet to be processed.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "--config", default=CONFIG_FILENAME, help="Name of XML config file."
    )

    # https://stackoverflow.com/a/47440202
    args = parser.parse_args(args=None if sys.argv[1:] else ["--help"])
    main(config_filename=args.config)
