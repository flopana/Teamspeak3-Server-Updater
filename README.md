# Teamspeak3 Server Updater
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

This python script is used to update your Teamspeak3 Server though it's not a difficult task having a script is convenient.
The python script also uses a local sqlite database for tracking the updates to avoid updating the server if not necessary.

## Installation
This script requires Python3 and pip to be installed.

Also this scripts folder should reside beside the teamspeak server folder for example:
```
└── usr
   └── local
      ├── teamspeak3-server-updater
      └── teamspeak3-server_linux_amd64
```
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
```
usage: python3 main.py [-h] [-v] [-f] [-u] [-a ARCHITECTURE]
Options:
  -h, --help                              Displays this message
  -v, --verbose                           Prints verbose output
  -f, --force                             Forces an update of the teamspeak server
  -u, --update                            The script updates itself
  -a, --architecture                      Lets you define the architecure (amd64 or x86)
```

## Advanced Usage:
Since the script also checks wether or not it should update you can automate it.

Example cronjob:
```
# Executes every Monday on 3AM
0 3 * * 1 cd /path/to/script && python3 main.py -u >/dev/null 2>&1
```
