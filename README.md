# Teamspeak3 Server Updater
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This is a python script is used to update your Teamspeak3 Server though it's not a difficult task having a script is convenient.
The python script also uses a local sqlite database to avoid updating the server if not necessary.

## Installation
This script requires Python3 and pip to be installed
```shell script
$ git clone https://github.com/flopana/teamspeak3-server-updater.git
$ cd teamspeak3-server-updater
$ pip install -r requirements.txt
```

## Usage
```shell script
$ python3 main.py
```

There are also options available
```shell script
usage: python3 main.py -h | -v
Options:
  -h, --help                              Displays this message
  -v, --verbose                           Prints verbose output
```