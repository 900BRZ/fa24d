import argparse

from .lib.csv import read


def main(data: str) -> None:
    laps = read(data)
    print("Data:", laps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process baseline and experiment files."
    )
    parser.add_argument("data", type=str, help="Path to the data file")

    args = parser.parse_args()

    main(args.data)
