# [Advent of Code](https://adventofcode.com/)

Advent of Code is an Advent calendar of small programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language you like. People use them as a speed contest, interview prep, company training, university coursework, practice problems, or to challenge each other.

This project contains solutions written by Toni Sredanović in Python programming language.

Check it out here: https://adventofcode.com/

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

### **solve**

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
  - if not provided then the real puzzle input will be used

#### Example usages
Solve a puzzle for year 2022, day 1, part a:
```
poetry run solve 2022 1 a
```

Solve a puzzle for year 2022, day 1, part a with test input file `2022_01_1_input.txt`:
```
poetry run solve 2022 1 a -d 1
```

### **gen-empty-solvers**

Generate empty solvers.

#### Arguments
- `year`
  - positional argument

#### Example usages
Generate empty solvers for year 2022:
```
poetry run gen-empty-solvers 2022
```

## License

These AoC solutions are a free software under terms of the `MIT License`.

Copyright (C) 2022 by [Toni Sredanović](https://tsredanovic.github.io/), toni.sredanovic@gmail.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
