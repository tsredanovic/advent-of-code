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

### Environment

Optional `.env` file can be created in `advent-of-code` directory with the following environment variables:
- `AOC_SESSION` - a cookie which is set when you login to AoC
- `AOCD_DIR` - directory where puzzle inputs, answers, names, and bad guesses are saved

More info about their use can be found here: https://pypi.org/project/advent-of-code-data/


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

## Scripts

### Solve

Solve a puzzle.

#### Arguments
- `year`
  - positional argument
- `day`
  - positional argument
  - valid choices: numbers `1` to `25`
- `part`
  - positional argument
  - valid choices: `a`, `b`
- `--data` (`-d`)
  - option that takes a value
  - value must be a input file name (`2022_01_1_input.txt`) or input file index (`1`) that exists
  - if not provided then the real input will be used

##### Example usages
Solve a puzzle for year 2022, day 1, part a:
```
poetry run solve 2022 1 a
```

Solve a puzzle for year 2022, day 1, part a with test input file `2022_01_1_input.txt`:
```
poetry run solve 2022 1 a -d 1
```