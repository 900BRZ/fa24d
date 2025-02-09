import pandas as pd

from .abstract_csv_reader import CsvReader
from ...lap import Lap
from ....mappings import ColumnMapping, profiles


class AimCsvReader(CsvReader):
    def pre_process_data(self, df):
        df["lap_number"] = 1
        return df

    def get_column_mapping(self) -> ColumnMapping:
        driver = self.metadata.get("User", None)
        if driver and driver and isinstance(driver, str) and driver in profiles:
            return profiles[driver]
        
        racer = self.metadata.get("Racer", None)
        if racer and racer and isinstance(racer, str) and racer in profiles:
            return profiles[racer]
        
        print(self.metadata)

        raise RuntimeError("No profile found for driver", driver, racer)


class AimSegmentCsvReader(AimCsvReader):
    def can_read(self) -> bool:
        format = self.metadata.get("Format", None)
        return (
            isinstance(format, str) and 
            format.lower() == "aim csv file"
            and "Beacon Markers" not in self.metadata
        )

    def split_laps(self, df: pd.DataFrame) -> list[Lap]:
        lap_time = float(df["time"].iloc[-1] - df["time"].iloc[0])
        return [Lap(data=df, filename=self.filepath, lap_number=1, lap_time=lap_time)]


class AimSessionCsvReader(AimCsvReader):
    def can_read(self) -> bool:
        format = self.metadata.get("Format", None)
        segment = self.metadata.get("Segment", None)

        return (
            isinstance(format, str) and 
            format.lower() == "aim csv file" and
            isinstance(segment, str) and
            segment == "Session"
            and "Beacon Markers" in self.metadata
        )

    def split_laps(self, df):
        lap_finish_timestamps = list(map(float, self.metadata["Beacon Markers"]))

        laps = []

        for i, _ in enumerate(lap_finish_timestamps):
            if i == 0:
                continue

            lap_time = float(lap_finish_timestamps[i] - lap_finish_timestamps[i - 1])
            lap_df = df[
                (df["time"] >= lap_finish_timestamps[i - 1])
                & (df["time"] < lap_finish_timestamps[i])
            ]

            laps.append(
                Lap(
                    data=lap_df,
                    filename=self.filepath,
                    lap_number=i,
                    lap_time=lap_time,
                )
            )

        return laps
