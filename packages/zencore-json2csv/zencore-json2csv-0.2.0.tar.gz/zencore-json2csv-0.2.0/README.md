# python-json2csv

Convert json array data to csv.

*Note:* zencore-json2csv rename to python-json2csv


## Install

    pip install python-json2csv


## Usage

    E:\>json2csv --help
    Usage: json2csv [OPTIONS]

    Options:
    -f, --file FILENAME     Input file name, use - for stdin.
    --file-encoding TEXT    Input file encoding.
    -o, --output FILENAME   Output file name, use - for stdout.
    --output-encoding TEXT  Output file encoding.
    -k, --keys TEXT         Output field names. Comma separated string list.
    -p, --path TEXT         Path of the data.
    --help                  Show this message and exit.

## Examples

### Example 1

**INPUT:**

    [
        [1,2,3],
        [2,3,4]
    ]

**OUTPUT:**

    1,2,3
    2,3,4

**COMMAND:**

    cat input.txt | json2csv -o output.txt

### Example 2

**INPUT:**

    [
        {"f1": 11, "f2": 12, "f3": 13},
        {"f1": 21, "f3": 23, "f2": 22}
    ]

**OUTPUT:**

    11,12,13
    21,22,23

**COMMAND:**

    cat input.txt | json2csv -o output.txt -k f1,f2,f3

### Example 3


**INPUT:**

    {
        "data": {
            "list": [
                [1,2,3],
                [2,3,4],
            ]
        }
    }

**OUTPUT:**

    1,2,3
    2,3,4

**COMMAND:**

    cat input.txt | json2csv -o output.txt -p data.list

## Releases

### v0.2.0 2019-11-05

- Rename from zencore-json2csv to python-json2csv.
- Fix console application install method in setup.py.

### v0.1.1 2018-02-27

- Simple json2csv console utils released.
