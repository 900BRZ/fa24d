import pandas as pd

from .abstract_csv_reader import CsvReader
from ...lap import Lap
from ....mappings import ColumnMapping, profiles


class RaceChronoCsvReader(CsvReader):

    def can_read(self) -> bool:
        with open(self.filepath) as f:
            first_line = f.readline()
            return first_line.startswith("This file is created using RaceChrono")

    def get_column_mapping(self) -> ColumnMapping:
        return profiles["racechrono"]

    def pre_process_data(self, df):
        # remove update frequency line
        return df[df.iloc[:, 0].notna()]

    def split_laps(self, df: pd.DataFrame) -> list[Lap]:
        laps = []
        grouped = df.groupby("lap_number")
        for lap_number, group in grouped:
            lap_time = float(group["time"].iloc[-1] - group["time"].iloc[0])
            laps.append(
                Lap(
                    data=group,
                    filename=self.filepath,
                    lap_number=int(float(lap_number)),
                    lap_time=lap_time,
                )
            )
        return laps
