from ..mappings import ColumnMapping, profiles


def test_reverse_mapping():
    mapping = ColumnMapping(
        time="Time",
        rpm="RPM",
        lap_number="",
        oil_p="OilPressure0",
        oil_t="OilTemp",
        gps_lat="GPS Latitude",
        gps_lon="GPS Longitude",
        gps_lat_acc="GPS LatAcc",
        gps_lon_acc="GPS LonAcc",
    )
    assert mapping.reverse_mapping("Time") == "time"
    assert mapping.reverse_mapping("RPM") == "rpm"
    assert mapping.reverse_mapping("OilPressure0") == "oil_p"
    assert mapping.reverse_mapping("OilTemp") == "oil_t"
    assert mapping.reverse_mapping("GPS Latitude") == "gps_lat"
    assert mapping.reverse_mapping("GPS Longitude") == "gps_lon"
    assert mapping.reverse_mapping("GPS LatAcc") == "gps_lat_acc"
    assert mapping.reverse_mapping("GPS LonAcc") == "gps_lon_acc"
