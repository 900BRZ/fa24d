from ..aim import AimSessionCsvReader, AimSegmentCsvReader
import numpy as np

SEGMENT_HEADER_CSV = "fixtures/aim_header.csv"
SESSION_HEADER_CSV = "fixtures/aim_header_multiline_comment.csv"
FULL_SESSION_CSV = "fixtures/aim_full_session.csv"


def test_session_reader_can_read():
    reader = AimSessionCsvReader(SEGMENT_HEADER_CSV)
    assert reader.can_read() == False

    reader = AimSessionCsvReader(SESSION_HEADER_CSV)
    assert reader.can_read() == True


def test_segment_reader_can_read():
    reader = AimSegmentCsvReader(SEGMENT_HEADER_CSV)
    assert reader.can_read() == True

    reader = AimSegmentCsvReader(SESSION_HEADER_CSV)
    assert reader.can_read() == False


def test_segment_reader_read():
    reader = AimSegmentCsvReader(SEGMENT_HEADER_CSV)
    laps = reader.read()

    assert len(laps) == 1
    assert laps[0].lap_number == 1
    assert laps[0].lap_time == 0.02
    assert round(laps[0].data["oil_t"].mean()) == 208  # f
    assert round(laps[0].data["oil_p"].mean()) == 77  # psi


def test_session_reader_read():
    reader = AimSessionCsvReader(FULL_SESSION_CSV)
    laps = reader.read()

    assert len(laps) == 7
    assert laps[0].lap_number == 1
    assert laps[3].lap_number == 4
    assert round(laps[3].lap_time) == 88
    assert round(laps[0].data["oil_t"].mean()) == 163  # f
    assert round(laps[0].data["oil_p"].mean()) == 62  # psi
