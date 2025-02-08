from ..metadata import count_metadata_lines, split_line, parse_metadata, parse_row


def test_line_with_quotes():
    example = '"Date","Sunday, March 10, 2024"'
    assert split_line(example) == ["Date", "Sunday, March 10, 2024"]


def test_line_without_quotes():
    example = "Date,Sunday March 10 2024"
    assert split_line(example) == ["Date", "Sunday March 10 2024"]


def test_line_without_value():
    example = "Date,"
    assert split_line(example) == ["Date", ""]


def test_line_with_multiple_values():
    example = '"Beacon Markers","629.768","740.742","852.571","1356"'

    assert split_line(example) == [
        "Beacon Markers",
        "629.768",
        "740.742",
        "852.571",
        "1356",
    ]


def test_parse_row():
    example = '"Beacon Markers","629.768","740.742","852.571","1356"'

    assert parse_row(example) == (
        "Beacon Markers",
        ["629.768", "740.742", "852.571", "1356"],
    )


def test_metadata_header_lines():
    assert count_metadata_lines("fixtures/aim_header.csv") == 12
    assert count_metadata_lines("fixtures/aim_header_multiline_comment.csv") == 18


def test_count_header_lines_from_seigo():
    result = parse_metadata("fixtures/aim_header.csv")
    expected = {
        "Format": "AIM CSV File",
        "Venue": "ThunderhS CA",
        "Vehicle": "BRZ",
        "User": "Seigo",
        "Data Source": "AIM Data Logger",
        "Comment": "Stock Tune V730",
        "Date": "01/04/25",
        "Time": "11:24:35",
        "Sample Rate": "50",
        "Duration": "119.814",
        "Segment": "Lap 2 - 1:59.814",
    }

    assert result == expected


def test_parse_metadata_with_multiline_comment():
    result = parse_metadata("fixtures/aim_header_multiline_comment.csv")

    expected = {
        "Format": "AiM CSV File",
        "Session": "Sonoma Raceway",
        "Vehicle": "2023 GR86 95",
        "Racer": "Kevin Schweigert",
        "Championship": "SpeedSF Challenge S4",
        "Comment": "8th day 235 40R18 SX2Annex CSP V1 7/8kNewly Repaved Track",
        "Date": "Sunday, March 10, 2024",
        "Time": "11:02 AM",
        "Sample Rate": "20",
        "Duration": "1356",
        "Segment": "Session",
        "Beacon Markers": ["629.768", "740.742", "852.571", "1356"],
        "Segment Times": ["10:29.768", "1:50.974", "1:51.829", "8:23.429"],
    }

    assert result == expected


def test_parse_metadata_from_race_chrono_file():
    result = parse_metadata("fixtures/racechrono_header.csv")
    expected = {
        "Format": "3",
        "Session title": "Thunderhill East, Bypass",
        "Session type": "Lap timing",
        "Track name": "Thunderhill East, Bypass",
        "Driver name": "",
        "Created": ["01/09/2024", "16:55"],
        "Note": "",
    }

    assert result == expected


def test_parse_metadata_from_full_aim_session():
    result = parse_metadata("fixtures/aim_full_session.csv")
    expected = {
        "Format": "AiM CSV File",
        "Session": "THill WST",
        "Vehicle": "2022 Subaru BRZ",
        "Racer": "Brian Armstrong",
        "Championship": "86 Challenge",
        "Comment": "",
        "Date": "Saturday, April 6, 2024",
        "Time": "2:36 PM",
        "Sample Rate": "20",
        "Duration": "1456",
        "Segment": "Session",
        "Beacon Markers": [
            "159.74",
            "523.752",
            "613.821",
            "703.609",
            "791.981",
            "880.531",
            "971.19",
            "1456",
        ],
        "Segment Times": [
            "2:39.740",
            "6:04.012",
            "1:30.069",
            "1:29.788",
            "1:28.372",
            "1:28.550",
            "1:30.659",
            "8:04.810",
        ],
    }

    assert result == expected


def test_count_metadata_lines_from_full_session():
    result = count_metadata_lines("fixtures/aim_full_session.csv")
    assert result == 14
