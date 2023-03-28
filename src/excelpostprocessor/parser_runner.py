"""
Module: contains class ParserRunner.
"""
import os

import xmltodict

from excelpostprocessor.excel_postprocessor import ExcelParser


class ParserRunner:
    """
    Handles the reading/parsing of config .xml file & creates/invokes ExcelParser objects to do the worksheet parsing.
    """

    def __init__(self, config_filename: str) -> None:
        if not isinstance(config_filename, str):
            raise TypeError("Argument 'config_filename' is not the expected string.")

        #   Parse config .xml file.
        if not os.path.exists(config_filename):
            raise FileExistsError(f"Unable to find file '{config_filename}'.")

        self.__config_filename = config_filename

    def process(self) -> None:
        with open(self.__config_filename, "r", encoding="utf-8") as file:
            my_xml = file.read()

            try:
                config = xmltodict.parse(my_xml)
            except Exception as e:
                raise SyntaxError(
                    f"Unable to read/parse file '{self.__config_filename}'."
                ) from e

        if "workbook" not in config:
            raise SyntaxError(
                f"Unable to find 'workbook' in file '{self.__config_filename}'."
            )

        workbook_config = config["workbook"]

        if "name" not in workbook_config:
            raise SyntaxError(
                f"Unable to find 'workbook/name' in file '{self.__config_filename}'."
            )

        target_filename = workbook_config["name"]

        if not os.path.exists(target_filename):
            raise FileExistsError(f"Unable to find file '{target_filename}'.")

        name, extension = os.path.splitext(os.path.basename(target_filename))

        if "sheet" not in workbook_config:
            raise SyntaxError(
                f"Unable to find 'workbook/sheet' in file '{self.__config_filename}'."
            )

        sheets_config = workbook_config["sheet"]

        #   If there's only one sheet, sheets_config will be a dict.
        #   Let's turn it into a single-element list.
        if isinstance(sheets_config, dict):
            sheets_config = [sheets_config]

        for this_sheet in sheets_config:
            if "name" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'name' for this sheet in file '{self.__config_filename}'."
                )

            #   We'll write out a new Excel workbook for every sheet, marked with the sheet name.
            sheet_name = this_sheet["name"]
            output_filename = os.path.join(
                os.path.dirname(target_filename), name + "_" + sheet_name + extension
            )

            excel_parser = ExcelParser(
                excel_filename=target_filename, sheet_name=sheet_name
            )

            if "source_column" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'source_column' for sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            column_config = this_sheet["source_column"]

            if "name" not in column_config:
                raise SyntaxError(
                    f"Unable to find 'name' for this source column in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            source_column_name = column_config["name"]

            if "extract" not in column_config:
                raise SyntaxError(
                    f"Unable to find 'extract' for column '{source_column_name}' in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            extracts_config = column_config["extract"]

            if isinstance(extracts_config, dict):
                extracts_config = [extracts_config]

            for this_extract in extracts_config:
                if "pattern" not in this_extract:
                    raise SyntaxError(
                        f"Unable to find 'pattern' for column '{source_column_name}' in sheet '{sheet_name}' "
                        f"in file '{self.__config_filename}'."
                    )

                if "new_column" not in this_extract:
                    raise SyntaxError(
                        f"Unable to find 'new_column' for column '{source_column_name}' in sheet '{sheet_name}' "
                        f"in file '{self.__config_filename}'."
                    )

                excel_parser.extract_into_new_column(
                    column_name=source_column_name,
                    pattern=this_extract["pattern"],
                    new_column=this_extract["new_column"],
                )

            #   Write out results for this worksheet.
            filename_created = excel_parser.write_to_excel(
                new_file_name=output_filename
            )
            print(f"Created file '{filename_created}'.")
