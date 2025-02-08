import pandas as pd

from ...lap import Lap
from .abstract_csv_reader import CsvReader


class AimSegmentCsvReader(CsvReader):
    def can_read(self) -> bool:
        return (
            "Format" in self.metadata
            and self.metadata["Format"].lower() == "aim csv file"
            and "Beacon Markers" not in self.metadata
        )
    
    def pre_process_data(self, df):
        df["lap_number"] = 1
        return df

    def split_laps(self, df: pd.DataFrame) -> list[Lap]:
        lap_time = float(df["time"].iloc[-1] - df["time"].iloc[0])
        return [Lap(data=df, filename=self.filepath, lap_number=1, lap_time=lap_time)]


class AimSessionCsvReader(CsvReader):
    def get_lap_metadata(self) -> pd.DataFrame:
        metadata = pd.read_csv(
            self.filepath, nrows=2, skiprows=11, header=None
        ).transpose()
        metadata.columns = ["marker", "lap_time"]
        metadata = metadata.drop(0)

        metadata["marker"] = metadata["marker"].astype(float)
        metadata["lap_time"] = metadata["lap_time"].apply(c.time_string_to_s)

        return metadata

    def pre_process_data(self, df):
        df["lap_number"] = 0
        return df

    def can_read(self) -> bool:
        return (
            "Format" in self.metadata
            and self.metadata["Format"].lower() == "aim csv file"
            and self.metadata["Segment"] == "Session"
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
