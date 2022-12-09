# [Advent of Code](https://adventofcode.com/)

Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as a speed contest, interview prep, company training, university coursework, practice problems, or to challenge each other.

This project contains solutions written by Toni Sredanović in Python programming language.


## Initialization

### Poetry

This project uses [Poetry](https://python-poetry.org/) for management.
For installation and usage see https://python-poetry.org/docs/.

Configure Poetry to create virtualenv inside the project’s root directory: 
```
poetry config virtualenvs.in-project true
```

Install dependencies: 
```
poetry install
```

## Formatting

This project uses [black](https://github.com/psf/black) for code formatting and [isort](https://pycqa.github.io/isort/index.html) for sorting imports.

Format code:
```
poetry run black .
```

Sort imports:
```
poetry run isort .
```

## Environment

Optional `.env` file can be created in `advent-of-code` directory with the following environment variables:
- `AOC_SESSION` - a cookie which is set when you login to AoC
- `AOCD_DIR` - directory where puzzle inputs, answers, names, and bad guesses are saved

More info about their use can be found here: https://pypi.org/project/advent-of-code-data/


