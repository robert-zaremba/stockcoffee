This repository contains two tools:

* `stock-stats.py` - tool to read stock prices either from local file or Yahoo Finance service and computes the geometric mean of all the Close prices there. The source must conform the Yahoo Finance historical stock prices CSV format.
* `stock-journal.py` - tool to do basic stock accounting and statistics.

# Requirements

Python3 >= 3.4 is required.

All dependencies to run the applications are specified in the `requirements.txt` file. Dev dependencies (to run tests) are in `requirements-dev.txt`

## Dependencies installation


### using pip

    pip install -r requirements.txt

if you want to run tests you need to install dev dependencies as well:

    pip install -r requirements-dev.txt

### Using setup.py (for development)

This will download and compile the numpy package so it's better to use the pip method above.

    python setup.py develop


# Usage

### stock-stats.py

    python stock-stats.py source

Where `source` is either the path to the CSV file conforming the Yahoo Finance historical stock prices format or name of a stock code. In the latter case the application will download the resources from Yahoo Finance service.

### stock-journal.py

This is an interactive application. Type `help` to get information about command. Type `help command` to get information about give command.
Tab completion is supported.

## Running tests

Just call the following command in the project root:

    py.test
