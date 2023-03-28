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

    def __extract_sheets_from_workbook(self, workbook_config: dict) -> list:
        if not isinstance(workbook_config, dict):
            raise TypeError("Argument 'workbook_config' is not the expected dict.")

        if "sheet" not in workbook_config:
            raise SyntaxError(
                f"Unable to find 'workbook/sheet' in file '{self.__config_filename}'."
            )

        sheets_config = workbook_config["sheet"]

        #   If there's only one sheet, sheets_config will be a dict.
        #   Let's turn it into a single-element list.
        if isinstance(sheets_config, dict):
            sheets_config = [sheets_config]

        return sheets_config

    def __extract_workbook_name(self, config: dict) -> str:
        """Gets the Excel workbook name from the config dictionary.

        Parameters
        ----------
        config : dict

        Returns
        -------
        workbook_name : str
        """
        if not isinstance(config, dict):
            raise TypeError("Argument 'config' is not the expected dict.")

        if "name" not in config:
            raise SyntaxError(
                f"Unable to find 'workbook/name' in file '{self.__config_filename}'."
            )

        workbook_name = config["name"]

        if not os.path.exists(workbook_name):
            raise FileExistsError(f"Unable to find file '{workbook_name}'.")

        return workbook_name

    def process(self) -> None:
        """Processes the job, reading the config file, setting up and running an ExcelParser object."""
        workbook_config = self.__read_config()
        source_filename = self.__extract_workbook_name(config=workbook_config)
        sheets_config = self.__extract_sheets_from_workbook(
            workbook_config=workbook_config
        )
        self.__process_sheets(sheets_config=sheets_config, source_file=source_filename)

    def __process_column(
        self, parser: ExcelParser, column_config: dict, sheet_name: str
    ) -> None:
        """Extracts the information for this column's processing & calls the ExcelParser object
        to parse & generate the new column.

        Parameters
        ----------
        column_config : dict    Defines the column name, regex and the name of the column to be created.

        """
        if not isinstance(parser, ExcelParser):
            raise TypeError("Argument 'parser' is not the expected ExcelParser object.")

        if not isinstance(column_config, dict):
            raise TypeError("Argument 'column_config' is not the expected dict.")

        if not isinstance(sheet_name, str):
            raise TypeError("Argument 'sheet_name' is not the expected str.")

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

            parser.extract_into_new_column(
                column_name=source_column_name,
                pattern=this_extract["pattern"],
                new_column=this_extract["new_column"],
            )

    def __process_sheets(self, sheets_config: list, source_file: str) -> None:
        """For each sheet, build the ExcelParser object aimed at that sheet & process all its columns.

        Parameters
        ----------
        sheets_config : list of dict objects, one per worksheet
        source_file : Excel workbook being processed
        """
        if not isinstance(sheets_config, list):
            raise TypeError("Argument 'sheets_config' is not the expected list.")

        if not isinstance(source_file, str):
            raise TypeError("Argument 'source_file' is not the expected str.")

        name, extension = os.path.splitext(os.path.basename(source_file))

        for this_sheet in sheets_config:
            if "name" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'name' for this sheet in file '{self.__config_filename}'."
                )

            #   We'll write out a new Excel workbook for every sheet, marked with the sheet name.
            sheet_name = this_sheet["name"]
            output_filename = os.path.join(
                os.path.dirname(source_file), name + "_" + sheet_name + extension
            )

            excel_parser = ExcelParser(
                excel_filename=source_file, sheet_name=sheet_name
            )

            if "source_column" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'source_column' for sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            column_config = this_sheet["source_column"]
            self.__process_column(
                parser=excel_parser, column_config=column_config, sheet_name=sheet_name
            )

            #   Write out results for this worksheet.
            filename_created = excel_parser.write_to_excel(
                new_file_name=output_filename
            )
            print(f"Created file '{filename_created}'.")

    def __read_config(self) -> dict:
        """Reads/parses the configuration .xml file.

        Returns
        -------
        config : dict       Describes how the workbook is to be parsed.
        """
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

        return config["workbook"]
