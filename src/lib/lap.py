from dataclasses import dataclass
import pandas as pd
from .conversions import s_to_time_string


@dataclass(kw_only=True)
class Lap:
    data: pd.DataFrame
    filename: str
    lap_number: int
    lap_time: float

    @property
    def humanized_time(self) -> str:
        return s_to_time_string(self.lap_time)
