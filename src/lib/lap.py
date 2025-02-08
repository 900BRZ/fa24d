from dataclasses import dataclass
import pandas as pd


@dataclass(kw_only=True)
class Lap:
    data: pd.DataFrame
    filename: str
    lap_number: int
    lap_time: float
