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

    def __column_name(self, column_config: dict, sheet_name: str) -> str:
        """Extracts the column name from the dict created from the .xml file.
        Assumes calling methods have screened inputs to be proper type.

        Parameters
        ----------
        column_config : dict
        sheet_name : str

        Returns
        -------
        column_name : str
        """
        if "name" not in column_config:
            raise SyntaxError(
                f"Unable to find 'name' for this source column in sheet '{sheet_name}' "
                f"in file '{self.__config_filename}'."
            )

        column_name = column_config["name"]
        return column_name

    def __extract_sheets_from_workbook(self, workbook_config: dict) -> list:
        """Pulls a list of sheet configuration dictionaries from the overall workbook config dict.

        Parameters
        ----------
        workbook_config : dict

        Returns
        -------
        sheets_config : list of dict
        """
        #   Can't exercise this type checking because it's already tested in the previous method.
        #   But leave this type check here in case modules get rearranged in the future.
        if not isinstance(workbook_config, dict):  # pragma: no cover
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

        if not isinstance(workbook_name, str) or not os.path.exists(workbook_name):
            raise FileExistsError(f"Unable to find file '{workbook_name}'.")

        return workbook_name

    def process(self) -> bool:
        """Processes the job, reading the config file, setting up and running an ExcelParser object.

        Returns
        -------
        success : bool   Did anything happen?
        """

        workbook_config = self.__read_config()
        source_filename = self.__extract_workbook_name(config=workbook_config)
        sheets_config = self.__extract_sheets_from_workbook(
            workbook_config=workbook_config
        )
        success: bool = self.__process_sheets(
            sheets_config=sheets_config, source_file=source_filename
        )
        return success

    def __process_column(
        self, parser: ExcelParser, column_config: dict, sheet_name: str
    ) -> bool:
        """Extracts the information for this column's processing & calls the ExcelParser object
        to parse & generate the new column.

        Parameters
        ----------
        column_config : dict    Defines the column name, regex and the name of the column to be created.

        Returns
        -------
        need_to_restore_column : bool   Lets calling method know we'll need to restore this column to its original value before writing out results.
        """
        if not isinstance(column_config, dict):
            raise TypeError("Argument 'column_config' is not the expected dict.")

        source_column_name = self.__column_name(
            column_config=column_config, sheet_name=sheet_name
        )

        if not isinstance(source_column_name, str):
            raise TypeError("Argument 'source_column_name' is not the expected str.")

        need_to_restore_column = False

        if "cleaning" in column_config:
            cleaning_config = column_config["cleaning"]

            if isinstance(cleaning_config, dict):
                cleaning_config = [cleaning_config]

            self.__process_column_cleaning(
                parser=parser,
                cleaning_rules=cleaning_config,
                sheet_name=sheet_name,
                column_name=source_column_name,
            )

            need_to_restore_column = True

        if "extract" not in column_config:
            raise SyntaxError(
                f"Unable to find 'extract' for column '{source_column_name}' in sheet '{sheet_name}' "
                f"in file '{self.__config_filename}'."
            )

        extracts_config = column_config["extract"]

        if isinstance(extracts_config, dict):
            extracts_config = [extracts_config]

        self.__process_column_extract(
            parser=parser,
            extracts=extracts_config,
            sheet_name=sheet_name,
            column_name=source_column_name,
        )

        return need_to_restore_column

    def __process_column_cleaning(
        self,
        parser: ExcelParser,
        cleaning_rules: list,
        sheet_name: str,
        column_name: str,
    ) -> None:
        for this_cleaning_rule in cleaning_rules:
            if "pattern" not in this_cleaning_rule:
                raise SyntaxError(
                    f"Unable to find 'pattern' for column '{column_name}' in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            if "replace" not in this_cleaning_rule:
                raise SyntaxError(
                    f"Unable to find 'replace' for column '{column_name}' in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            parser.clean_column(
                column_name=column_name,
                pattern=this_cleaning_rule["pattern"],
                replace=this_cleaning_rule["replace"],
            )

    def __process_column_extract(
        self, parser: ExcelParser, extracts: list, sheet_name: str, column_name: str
    ) -> None:
        for this_extract in extracts:
            if "pattern" not in this_extract:
                raise SyntaxError(
                    f"Unable to find 'pattern' for column '{column_name}' in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            if "new_column" not in this_extract:
                raise SyntaxError(
                    f"Unable to find 'new_column' for column '{column_name}' in sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            parser.extract_into_new_column(
                column_name=column_name,
                pattern=this_extract["pattern"],
                new_column=this_extract["new_column"],
            )

    def __process_sheets(self, sheets_config: list, source_file: str) -> bool:
        """For each sheet, build the ExcelParser object aimed at that sheet & process all its columns.

        Parameters
        ----------
        sheets_config : list of dict objects, one per worksheet
        source_file : Excel workbook being processed

        Returns
        -------
        success : bool  Did it work?
        """
        success_per_sheet = []

        name, extension = os.path.splitext(os.path.basename(source_file))

        for this_sheet in sheets_config:
            if "name" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'name' for this sheet in file '{self.__config_filename}'."
                )

            #   We'll write out a new Excel workbook for every sheet, marked with the sheet name.
            sheet_name = this_sheet["name"]

            #   In case it's None.
            if not isinstance(sheet_name, str):
                raise TypeError("Argument 'sheet_name' is not the expected str.")

            output_filename = os.path.join(
                os.path.dirname(source_file), name + "_" + sheet_name + extension
            )

            #   Try to instantiate an ExcelParser object for this sheet name,
            #   but there's no guarantee the sheet exists in the Excel file,
            #   so we'll trap the error & skip the sheet.
            try:
                excel_parser = ExcelParser(
                    excel_filename=source_file, sheet_name=sheet_name
                )
            except ValueError:
                print(f"Worksheet {sheet_name} not found; skipping.")
                success_per_sheet.append(False)
                continue

            if "source_column" not in this_sheet:
                raise SyntaxError(
                    f"Unable to find 'source_column' for sheet '{sheet_name}' "
                    f"in file '{self.__config_filename}'."
                )

            column_config = this_sheet["source_column"]
            need_to_restore_column = self.__process_column(
                parser=excel_parser, column_config=column_config, sheet_name=sheet_name
            )

            if need_to_restore_column:
                source_column_name = self.__column_name(
                    column_config=column_config, sheet_name=sheet_name
                )
                excel_parser.restore_original_column(column_name=source_column_name)

            #   Write out results for this worksheet.
            filename_created = excel_parser.write_to_excel(
                new_file_name=output_filename
            )
            print(f"Created file '{filename_created}'.")
            success_per_sheet.append(True)

        return all(success_per_sheet)

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
