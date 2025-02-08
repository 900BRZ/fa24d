import pandas as pd
import os
from io import StringIO


def read_last_line(file_path: str) -> str:
    """
    Reads the last line of a CSV file without loading the whole file into memory.
    """
    with open(file_path, "rb") as file:
        file.seek(-2, os.SEEK_END)
        while file.read(1) != b"\n":
            file.seek(-2, os.SEEK_CUR)
        return file.readline().decode()


def csv_width(file_path: str) -> int:
    """
    Returns the number of columns in a CSV file based on the final line, which should be representative of the data in the whole file, ignoring metadata.
    """
    last_line = read_last_line(file_path)
    df = pd.read_csv(StringIO(last_line))
    return df.shape[1]


def downsample(df: pd.DataFrame, *, downsample_factor: int = 1) -> pd.DataFrame:
    return df[::downsample_factor]
