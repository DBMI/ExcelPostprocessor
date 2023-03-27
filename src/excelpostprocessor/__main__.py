"""
    Excel Postprocessor applies Regular Expressions to an existing Excel workbook, extracting data into a new column.
"""
import argparse
from parser_runner import ParserRunner

CONFIG_FILENAME = "excel_postprocessor.xml"


def main() -> None:
    #   Handle 'help' case.
    parser = argparse.ArgumentParser(
        description="""Excel Postprocessor applies Regular Expressions to an existing Excel workbook,
         extracting data into a new column.
         Provide a configuration file named 'excelpostprocessor.xml' that provides:
         \n1) Name of the Excel workbook
         \n2) Sheet(s) to be processed
         \n3) The Regular Expression to use and the new column to be created.
         
         Here's an example file:
         
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
        </workbook>""",
        epilog="""Running the executable excelpostprocessor.exe without arguments will cause it to read and parse 
        the .xml config file, creating a new Excel workbook for each worksheet to be processed.""",
    )
    parser.parse_args()

    runner = ParserRunner(config_filename=CONFIG_FILENAME)
    runner.run()


if __name__ == "__main__":
    main()
