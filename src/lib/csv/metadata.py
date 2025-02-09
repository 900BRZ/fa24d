from .utils import csv_width
from enum import Enum
from functools import lru_cache


def count_metadata_lines(filepath: str) -> int:
    """
    Counts the number of metadata lines in a CSV file. We expect these have a different number of columns to the file data.
    """
    cols = csv_width(filepath)

    with open(filepath, "r") as file:
        i = 0
        while True:
            line = file.readline()
            if line.endswith(",\n"):
                line = line[:-2] + "\n"
            if line.count(",") == cols - 1:
                return i
            i += 1
    return 0


class QuoteType(str, Enum):
    SINGLE = "'"
    DOUBLE = '"'


def split_line(s: str) -> list[str]:
    """
    Accepts a variety of different formats, including quoted or unquoted strings and variable columns.
    """
    seen_quote: QuoteType | None = None
    acc: list[str] = []
    current: list[str] = []

    for char in s:
        if char == "\n":
            continue
        if seen_quote:
            if char == seen_quote.value:
                seen_quote = None
            else:
                current += char
        else:
            if char in [QuoteType.SINGLE.value, QuoteType.DOUBLE.value]:
                seen_quote = QuoteType(char)
            elif char == ",":
                acc.append("".join(current))
                current = []
            else:
                current += char

    return acc + ["".join(current)]


def parse_row(row: str) -> tuple[str, str | list[str]] | None:
    """
    Turns a row into a key/value pair, ignoring lines without a value and handling multiple values.
    """
    items = split_line(row)
    if len(items) < 2:
        return None
    key = items[0]
    values = items[1:]
    return key, values[0] if len(values) == 1 else values


@lru_cache
def parse_metadata(filepath: str) -> dict[str, str | list[str]]:
    """
    Parses metadata from a CSV file, making no attempt to cast values or normalize keys.
    """
    header_size = count_metadata_lines(filepath)

    metadata = {}

    with open(filepath, "r") as f:
        lines_left = header_size
        while lines_left > 0:
            line = f.readline()
            lines_left -= 1
            while line.count('"') % 2 != 0:
                next_line = f.readline()
                lines_left -= 1
                if not next_line:
                    break
                line = line.rstrip("\n") + next_line.rstrip("\n")
            row = parse_row(line)
            if row:
                metadata[row[0]] = row[1]

    return metadata
