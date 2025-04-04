set positional-arguments

workspace := `pwd`

[private]
default:
  @just --list

# Autoformat python code
format:
  poetry run black .

# Run all checks
check: check-black check-mypy

# Check formatting
check-black:
  poetry run black --check .

# Check types (mypy)
check-mypy:
  poetry run mypy .

# Check types (pyre)
check-pyre:
  poetry run pyre check

# Run tests
test +args=".":
  poetry run pytest "$@"

# Compare two data files, with the first being the baseline and the second being the experiment
compare +args:
  poetry run python -m src.compare "$@"

inspect +args:
  poetry run python -m src.inspect "$@"

# View a single data file
view +args:
  poetry run python -m src.view "$@"

dev:
  poetry run fastapi dev src/main.py
