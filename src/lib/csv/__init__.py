from .reader.race_chrono import RaceChronoCsvReader
from .reader.aim import AimSegmentCsvReader, AimSessionCsvReader
from ..lap import Lap

readers = [RaceChronoCsvReader, AimSessionCsvReader, AimSegmentCsvReader]


class UnsupportedFileType(RuntimeError):
    pass


def read(file_path: str) -> list[Lap]:
    for reader_cls in readers:
        reader = reader_cls(file_path)
        if reader.can_read():
            print("[debug] reading from", reader)
            return reader.read()
    raise UnsupportedFileType("This file type has no valid readers")
