from ..race_chrono import RaceChronoCsvReader
import numpy as np

SEGMENT_HEADER_CSV = "fixtures/aim_header.csv"
SESSION_HEADER_CSV = "fixtures/aim_header_multiline_comment.csv"
FULL_SESSION_CSV = "fixtures/aim_full_session.csv"


def test_can_read():
    reader = RaceChronoCsvReader("fixtures/racechrono_header.csv")
    assert reader.can_read() == True


def test_read():
    reader = RaceChronoCsvReader("fixtures/racechrono_header.csv")
    laps = reader.read()

    assert len(laps) == 1
    assert laps[0].lap_number == 1
    assert laps[0].lap_time == 0.026999950408935547
    assert round(laps[0].data["oil_t"].mean()) == 208  # f
    assert round(laps[0].data["oil_p"].mean()) == 75  # psi


def test_read_full_session():
    reader = RaceChronoCsvReader("fixtures/racechrono_full_session.csv")
    laps = reader.read()

    assert len(laps) == 3
    assert laps[1].lap_number == 2
    assert round(laps[1].lap_time) == 130
    assert round(laps[1].data["oil_t"].mean()) == 219  # f
    assert round(laps[1].data["oil_p"].mean()) == 72  # psi
