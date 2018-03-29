# Pyrrot

Python Rotten Requirements

## Install

```bash
pip install git+https://github.com/Leryan/pyrrot
```

## Usage

```bash
pyrrot -r requirements.txt [--json]
```

## Example

```
$ pyrrot -r ~/someproject/requirements.txt
Beaker: wants: <1.6.0, latest is 1.9.0
influxdb: wants: ==2.12.0, latest is 5.0.0
pymongo: wants: <2.9.0, latest is 3.6.1
python-ldap: wants: <3.0.0, latest is 3.0.0
```

```
$ pyrrot -r ~/someproject/requirements.txt --jsonç
...cool json output you can use to do your own job...
```