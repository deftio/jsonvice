[![PyPI version](https://badge.fury.io/py/jsonvice.svg)](https://badge.fury.io/py/jsonvice)
[![Build Status](https://api.travis-ci.com/deftio/jsonvice.svg?branch=master)](https://app.travis-ci.com/deftio/jsonvice)
[![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)


# About jsonvice  

jsonvice is command line tool for minifying JSON with optimal precision truncation/rounding.  In many applications floating point values in JSON can be very long (15 digits or more) but this level of accuracy isn't needed and takes up much space.

jsonvice allows the truncation of all the embedded floating point numbers (wherever they appear) to a specified number of digits. 

It also removes unnecessary white space to minify JSON files.

sample_input.json
```json
{
    "x" :   12.32,
    "y": 0.23482498323433,
    "z": "simple test",
    "a" : [ 1, 2, 3.23423434343 ]
}
```

now run jsonvice
```sh
jsonvice -i input.json -o output.json -p 4
```

ouput.json
```json
{"x":12.32,"y":0.2348,"z":"simple test","a":[1,2,3.2342]}
```


# More Examples

compactify json and reduce floating point precision to max of 5 digits by rounding
```shell
jsonvice -i sample_input.json -o output.json -p 5
```

compactify json and reduce floating point precision to max of 5 digits by rounding down
```shell
jsonvice -i myfile.json -o output.json -p 5 -q floor
```

jsonvice also allows stdin / stdout pipes to be used
```shell
cat simple_test.json | python3 path/to/jsonvice.py -i - -o - > output_test.json
```

jsonvice can also beautify (pretty print) json, while still performing precision truncation.  Note this makes the file larger.
```shell
jsonvice -i myfile.json -o output.json -p 3 -b
```


# Building and Source
All source is at [jsonvice](https://github.com/deftio/jsonvice)

jsonvice is built with Python using the Poetry packaging and build tool.

pip3 install poetry  # if not installed.

poetry update
poetry install
poetry build

poetry run jsonvice ...parameters...

Example
```sh
poetry run jsonvice -i inputfile.json -o outputfile.json -p 4
```



# Installing as stand alone commandline tool
pip can be used into install jsonvice as stand alone tool (note python 3.6 should or later specified)
```sh
pip install jsonvice
```

### pipx install
pipx can be used to install a stand alone version of jsonvice as a command line tool. Note pipx is like pip or pip3 but installs programs with their own virtual environment.

```sh
pipx install jsonvice
```

or install from github repo 

```sh
pipx install git+https://github.com/deftio/jsonvice
```

Now you can use jsonvice at the commandline without typing python3 like this example:

```
jsonvice -i inputfile.json -o - -b
```

## Python version support
Python version 3.6 or higher is required to build jsonvice.  If pipx is used for install isolation takes place automatically.

# Testing
Both pytest and tox were used to build jsonvice.  Testing can be performed at the command line via either tool:

```sh
poetry run pytest
```
or
```sh
tox
```

# History & Motivation
json vice started as a script to compactify / minify some large machine learning model files which had large floating point numbers.   By rounding to fixed number of sig digits and then testing the models against testsuites to see the effects of truncation.

At the time couldn't find a tool and whipped up small script (the original script is in /dev directory).

So jsonvice was built to learn / test practices around the python poetry and pipx tools, for use in other projects, but starting with a small example cli program that already worked.  

# License
jsonvice uses the BSD-2 open source license
