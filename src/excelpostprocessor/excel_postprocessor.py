"""
Moodule: contains class ExcelParser.
"""
import os

import openpyxl
import pandas
from typing import Union


class ExcelParser:
    """
    Reads existing Excel spreadsheet, parses desired targets & adds columns.
    """

    def __init__(self, excel_filename: str, sheet_name: str = None) -> None:
        """Reads in one sheet of the Excel file.

        Parameters
        ----------
        excel_filename : str        Name of existing Excel file
        sheet_name : Optional str   If not specified, reads first sheet.
        """
        if not isinstance(excel_filename, str):
            raise TypeError("Argument 'excel_filename' is not the expected str.")

        if not os.path.isfile(excel_filename):
            raise FileNotFoundError(f"Unable to find file '{excel_filename}'.")

        self.__excel_filename = excel_filename

        if not isinstance(sheet_name, str):
            #   Look up active sheet name.
            wb = openpyxl.load_workbook(self.__excel_filename)
            sheet_name = wb.active.title
            wb.close()

        self.__sheet_name = sheet_name
        self.__df: pandas.DataFrame = pandas.read_excel(
            self.__excel_filename, sheet_name=sheet_name
        )
        self.__df_orig: pandas.DataFrame = self.__df.copy()

        if not isinstance(self.__df, pandas.DataFrame):  # pragma: no cover
            raise RuntimeError(f"Unable to read file '{self.__excel_filename}'.")

    def clean_column(self, column_name: str, pattern: str, replace: str) -> None:
        """Use a regex to fix strings.

        Parameters
        ----------
        column_name : str
        pattern : str
        replace : str
        """

        if column_name not in self.__df:
            raise AttributeError(f"Unable to find column '{column_name}' in DataFrame.")

        revised_series = self.__df[column_name].str.replace(
            pattern, replace, regex=True
        )
        self.__df[column_name] = revised_series

    def data(self) -> pandas.DataFrame:
        """Allows read access to self.__df.

        Returns
        -------
        df : pandas.DataFrame
        """
        return self.__df

    def extract(self, column_name: str, pattern: str) -> list:
        """Use a regex to extract data from a given column into a list.

        Parameters
        ----------
        column_name : str
        pattern : str

        Returns
        -------
        extracted_data : list of str
        """
        extracted_data = self.__extract_series(column_name=column_name, pattern=pattern)
        return extracted_data.tolist()

    def extract_into_new_column(
        self, column_name: str, pattern: Union[str, list], new_column: str
    ) -> None:
        """Use a regex to extract data from a given column into a new column.

        Parameters
        ----------
        column_name : str
        pattern : str or list of str
        new_column : str
        """
        if not isinstance(column_name, str):
            raise TypeError("Argument 'column_name' is not the expected str.")

        if column_name not in self.__df:
            raise AttributeError(f"Unable to find column '{column_name}' in DataFrame.")

        if not isinstance(new_column, str):
            raise TypeError("Argument 'new_column' is not the expected str.")

        if isinstance(pattern, list):
            #   Try each pattern & use the values for the rows when it matches.
            extracted_data = pandas.Series(dtype="float64")

            for this_pattern in pattern:
                this_extracted_data = self.__extract_series(
                    column_name=column_name, pattern=this_pattern
                )

                if extracted_data.empty:
                    extracted_data = this_extracted_data
                else:
                    extracted_data.update(this_extracted_data)
        else:
            extracted_data = self.__extract_series(
                column_name=column_name, pattern=pattern
            )

        self.__df[new_column] = extracted_data

        #   The source column is almost always a long string, and it's more convenient if
        #   it stays the last column (so the long text doesn't overwrite the new extracted column).
        #   So rearrange the dataframe columns to put the source column last.
        cols = list(self.__df.columns.values)
        rearranged_cols = [c for c in cols if c != column_name]
        rearranged_cols.append(column_name)
        self.__df = self.__df[rearranged_cols]

    def __extract_series(self, column_name: str, pattern: str) -> pandas.Series:
        """Extracts column to Series using regex.

        Parameters
        ----------
        column_name : str
        pattern : str

        Returns
        -------
        column : Series
        """
        if not isinstance(column_name, str):
            raise TypeError("Argument 'column_name' is not the expected str.")

        if not isinstance(pattern, str):
            raise TypeError("Argument 'pattern' is not the expected str.")

        if column_name not in self.__df:
            raise AttributeError(f"Unable to find column '{column_name}' in DataFrame.")

        column: pandas.Series = self.__df[column_name].str.extract(pattern).squeeze()
        return column

    def restore_original_column(self, column_name: str) -> None:
        """Restores the original (uncleaned) column in preparation for writing out results.
        In (optional) cleaning, we may have changed the source column in the dataframe.
        But when writing out the results, we want to show the original column.

        Parameters
        ----------
        column_name : str
        """

        if column_name not in self.__df:
            raise AttributeError(
                f"Unable to find column '{column_name}' in modified DataFrame."
            )

        if column_name not in self.__df_orig:
            raise AttributeError(
                f"Unable to find column '{column_name}' in original DataFrame."
            )

        self.__df[column_name] = self.__df_orig[column_name]

    def write_to_excel(self, new_file_name: str = None) -> str:
        """Write out the dataframe we've been building.

        Parameters
        ----------
        new_file_name : Optional str

        Returns
        -------
        new_file_name : str
        """
        if not new_file_name:
            name, extension = os.path.splitext(os.path.basename(self.__excel_filename))
            new_file_name = os.path.join(
                os.path.dirname(self.__excel_filename), name + "_revised" + extension
            )

        # https: // stackoverflow.com / a / 72446796 / 18749636
        wb_obj = openpyxl.Workbook()
        wb_obj.save(new_file_name)
        sheet = wb_obj.active
        sheet.title = self.__sheet_name
        start_col = 1
        start_row = 1
        col_idx = start_col

        # insert values
        for label, content in self.__df.items():
            sheet.cell(row=start_row, column=col_idx, value=label)

            for row_idx, value_ in enumerate(content):
                sheet.cell(row=start_row + row_idx + 1, column=col_idx, value=value_)

            col_idx += 1

        wb_obj.save(new_file_name)
        return new_file_name
