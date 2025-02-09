from dataclasses import dataclass


@dataclass
class ColumnMapping:
    time: str
    rpm: str
    lap_number: str
    oil_p: str
    oil_t: str
    gps_lat: str
    gps_lon: str
    gps_lat_acc: str
    gps_lon_acc: str

    def __post_init__(self):
        self._reverse_mapping = {v: k for k, v in self.__dict__.items()}

    def reverse_mapping(self, value: str) -> str:
        return self._reverse_mapping.get(value)


# check for racer, check for user, check for racechrono

profiles = {
    "Brian Armstrong": ColumnMapping(
        time="Time",
        rpm="RPM",
        lap_number="lap_number",
        oil_p="OilPressure0",
        oil_t="OilTemp",
        gps_lat="GPS Latitude",
        gps_lon="GPS Longitude",
        gps_lat_acc="GPS LatAcc",
        gps_lon_acc="GPS LonAcc",
    ),
    "Seigo": ColumnMapping(
        time="Time",
        rpm="RPM",
        lap_number="lap_number",
        oil_p="OilPressure1",
        oil_t="OilTemp",
        gps_lat="GPS_Latitude",
        gps_lon="GPS_Longitude",
        gps_lat_acc="GPS_LatAcc",
        gps_lon_acc="GPS_LonAcc",
    ),
    "Kevin Schweigert": ColumnMapping(
        time="Time",
        rpm="RPM",
        lap_number="lap_number",
        oil_p="OilPressure0",
        oil_t="OilTemp",
        gps_lat="GPS Latitude",
        gps_lon="GPS Longitude",
        gps_lat_acc="GPS LatAcc",
        gps_lon_acc="GPS LonAcc",
    ),
    "racechrono": ColumnMapping(
        time="timestamp",
        rpm="rpm",
        lap_number="lap_number",
        oil_p="engine_oil_pressure_1",
        oil_t="engine_oil_temp",
        gps_lat="latitude",
        gps_lon="longitude",
        gps_lat_acc="lateral_acc",
        gps_lon_acc="longitudinal_acc",
    ),
}
