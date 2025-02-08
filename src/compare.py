import argparse

from .lib.csv import read


def main(baseline: str, experiment: str) -> None:
    laps = read(baseline)
    print("Baseline:", laps)

    laps = read(experiment)
    print("Experiment:", laps)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process baseline and experiment files."
    )
    parser.add_argument("baseline", type=str, help="Path to the baseline file")
    parser.add_argument("experiment", type=str, help="Path to the experiment file")

    args = parser.parse_args()

    main(args.baseline, args.experiment)
