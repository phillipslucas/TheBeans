"""This module imports a csv as a pandas dataframe."""
import pandas as pd

def csv_to_df(csv_file):
    """Converts a csv file to a pandas dataframe.

    Args:
        csv (str): The path to the csv file.

    Returns:
        pd.DataFrame: The pandas dataframe.
    """
    return pd.read_csv(csv_file)