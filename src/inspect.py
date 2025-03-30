import argparse

from .lib.csv import read


def main(file: str) -> None:
    laps = read(file)

    for lap in laps:
        print(f"{lap.lap_number}:{lap.humanized_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="View metadata for file"
    )
    parser.add_argument("file", type=str, help="Path to the csv")
    args = parser.parse_args()

    main(args.file)
