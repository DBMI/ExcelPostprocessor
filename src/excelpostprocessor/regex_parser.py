"""
Module: contains class RegexParser.
"""
from typing import Union

import pandas


class RegexParser:
    """
    Handles the details of applying regular expressions to a Pandas DataFrame.
    """

    def __init__(self, df: pandas.DataFrame):
        if not isinstance(df, pandas.DataFrame):
            raise TypeError(
                "Argument 'df' is not the expected pandas.DataFrame object."
            )

        self.__df = df
        self.__df_orig = df.copy()

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

    def extract(self, column_name: str, pattern: Union[str, list]) -> list:
        """Use a regex to extract data from a given column into a list.

        Parameters
        ----------
        column_name : str
        pattern : str

        Returns
        -------
        extracted_data : list of str
        """
        if not isinstance(column_name, str):
            raise TypeError("Argument 'column_name' is not the expected str.")

        if column_name not in self.__df:
            raise AttributeError(f"Unable to find column '{column_name}' in DataFrame.")

        if not isinstance(pattern, str) and not isinstance(pattern, list):
            raise TypeError("Argument 'pattern' is neither the expected str nor list.")

        extracted_data = self.__extract(column_name=column_name, pattern=pattern)
        return extracted_data.tolist()

    def __extract(self, column_name: str, pattern: Union[str, list]) -> pandas.Series:
        """Handles the extraction of data for either extract or extract_into_new_column methods.
        Assumes the calling methods have screened inputs for proper type.

        Parameters
        ----------
        column_name : str
        pattern : str or list of str

        Returns
        -------
        extracted_data : pandas.Series
        """
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

        return extracted_data

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

        if not isinstance(pattern, str) and not isinstance(pattern, list):
            raise TypeError("Argument 'pattern' is neither the expected str nor list.")

        if not isinstance(new_column, str):
            raise TypeError("Argument 'new_column' is not the expected str.")

        extracted_data = self.__extract(column_name=column_name, pattern=pattern)
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
        Assumes the calling methods have screened inputs for proper type.

        Parameters
        ----------
        column_name : str
        pattern : str

        Returns
        -------
        column : Series
        """
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
        if not isinstance(column_name, str):
            raise TypeError("Argument 'column_name' is not the expected str.")

        if column_name not in self.__df:
            raise AttributeError(
                f"Unable to find column '{column_name}' in modified DataFrame."
            )

        # There's no way the 'orig' dataframe could not contain this column,
        #  but you never know!
        if column_name not in self.__df_orig:  # pragma no cover
            raise AttributeError(
                f"Unable to find column '{column_name}' in original DataFrame."
            )

        self.__df[column_name] = self.__df_orig[column_name]
