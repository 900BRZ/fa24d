from ...lap import Lap
from ...conversions import kpa_to_psi, c_to_f

from abc import ABC, abstractmethod
from ..metadata import parse_metadata, count_metadata_lines
import pandas as pd

column_rename_mapping = {
    "timestamp": "time",
    "lapnumber": "lap_number",
    "engineoilpressure1": "oil_p",
    "oilpressure0": "oil_p",
    "oilpressure": "oil_p",
    "oilp": "oil_p",
    "oiltemp": "oil_t",
    "engineoiltemp": "oil_t",
    "oiltemperature": "oil_t",
    "oilt": "oil_t",
    "latitude": "gps_lat",
    "longitude": "gps_lon",
    "gpslatitude": "gps_lat",
    "gpslongitude": "gps_lon",
    "gpslat": "gps_lat",
    "gpslon": "gps_lon",
    "gpslng": "gps_lon",
    "gpslatacc": "gps_lat_acc",
    "gpslngacc": "gps_lon_acc",
    "gpslonacc": "gps_lon_acc",
    "gpslngaccel": "gps_lon_acc",
    "gpslonaccel": "gps_lon_acc",
    "lateralacc": "gps_lat_acc",
    "longitudinalacc": "gps_lon_acc",
}


def column_rename(col_name: str) -> str:
    s = col_name.lower().replace(" ", "").replace("_", "")
    if s in column_rename_mapping:
        return column_rename_mapping[s]
    return col_name.lower().replace(" ", "_")


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


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    return df.rename(columns=column_rename, inplace=False)


def drop_irrelevant_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[columns_to_keep]


def normalize_units(df: pd.DataFrame, units: list[str]) -> pd.DataFrame:
    for col in units:
        if col not in df.columns:
            continue
        df[col] = df[col].apply(unit_fn_map.get(col, lambda x: x))
    return df


class CsvReader(ABC):
    filepath: str

    def __init__(self, filepath: str):
        self.filepath = filepath

    @property
    def metadata(self) -> dict:
        return parse_metadata(self.filepath)

    def normalize_csv(self, df: pd.DataFrame) -> pd.DataFrame:
        # drop first row if it matches the header row (happens in some AiM files)
        if isinstance(df.iloc[0, 0], str) and df.iloc[0, 0] == df.columns[0]:
            df = df.drop(0).reset_index(drop=True)

        df = normalize_column_names(df)
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
        df['time_index'] = pd.to_datetime(df['time'], unit='s')
        df.set_index("time_index", inplace=True)          
        df.resample('20ms').mean()

        return df

    @abstractmethod
    def split_laps(self, df: pd.DataFrame) -> list[Lap]:
        pass

    @abstractmethod
    def can_read(self) -> bool:
        pass

    def pre_process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

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

        return self.split_laps(df)
