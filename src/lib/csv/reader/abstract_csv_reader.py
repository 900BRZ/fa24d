import pandas as pd
import numpy as np
from typing import Protocol

from ..metadata import parse_metadata, count_metadata_lines
from ...lap import Lap
from ...conversions import kpa_to_psi, c_to_f
from ....mappings import ColumnMapping


columns_to_keep = [
    "time",
    "lap_number",
    "rpm",
    "oil_p",
    "oil_t",
    "gps_lat",
    "gps_lon",
    "gps_lat_acc",
    "gps_lon_acc",
]

unit_fn_map = {
    "kPa": kpa_to_psi,
    "°C": c_to_f,
    "C": c_to_f,
    ".C": c_to_f,
}


def drop_irrelevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[columns_to_keep]


def normalize_units(df: pd.DataFrame, units: list[str]) -> pd.DataFrame:
    for i, col in enumerate(df.columns):
        units_for_column = units[i]
        df[col] = df[col].apply(unit_fn_map.get(units_for_column, lambda x: x))
    return df


def normalized_pressure_drop(actual: float, expected: float) -> float:
    return min(actual / expected, 1) * 100


class CsvReader(Protocol):
    def can_read(self) -> bool: ...
    def get_column_mapping(self) -> ColumnMapping: ...
    def split_laps(self, df: pd.DataFrame) -> list[Lap]: ...

    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    @property
    def metadata(self) -> dict[str, str | list[str]]:
        return parse_metadata(self.filepath)

    def normalize_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=self.get_column_mapping().reverse_mapping)

    def normalize_csv(self, df: pd.DataFrame) -> pd.DataFrame:
        # drop first row if it matches the header row (happens in some AiM files)
        if isinstance(df.iloc[0, 0], str) and df.iloc[0, 0] == df.columns[0]:
            df = df.drop(0).reset_index(drop=True)

        df = self.normalize_column_names(df)
        assert "time" in df.columns, f"Time column not found in {df.columns}"

        df = drop_irrelevant_columns(df)
        df = df[df.iloc[:, 0].notna()]

        units = df.iloc[0].to_list()
        df = df.drop(0).reset_index(drop=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        df = normalize_units(df, units)

        # drop leading empty lines manually due to metadata section sometimes containing empty lines
        while pd.isna(df.iloc[0, 0]):
            df = df.drop(0).reset_index(drop=True)

        # normalize data frequency
        df["time_index"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time_index", inplace=True)
        df.resample("50ms").mean()

        return df

    def pre_process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def post_process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    def perform_lap_analysis(self, lap: Lap) -> None:
        filtered_data = lap.data.query(
            "gps_lat_acc < 0.3 and rpm > 4500", inplace=False
        )
        oil_p_regression_line = np.polyfit(
            filtered_data["oil_t"], filtered_data["oil_p"], 1
        )
        m, b = oil_p_regression_line
        lap.data = lap.data.copy()
        lap.data["expected_oil_p"] = m * lap.data["oil_t"] + b
        lap.data["normalized_oil_p_drop_percent"] = lap.data.apply(
            lambda row: normalized_pressure_drop(row["oil_p"], row["expected_oil_p"]),
            axis=1,
        )

    def read(self) -> list[Lap]:
        metadata_lines = count_metadata_lines(self.filepath)

        df = pd.read_csv(
            self.filepath,
            header=0,
            skiprows=metadata_lines,
            skip_blank_lines=False,
            low_memory=False,
        )

        df = self.pre_process_data(df)
        df = self.normalize_csv(df)
        df = self.post_process_data(df)

        laps = self.split_laps(df)

        for lap in laps:
            self.perform_lap_analysis(lap)

        return laps
