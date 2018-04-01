# Pyrrot

Python Rotten Requirements

 * Supports `pypi.python.org` as remote repository by default, by lets you write your own remote checker, see the `RemotePyPi` class
 * Supports "human" and JSON output, also lets you write your own printer, see the `HumanPrinter` class
 * Uses the [packaging](https://github.com/pypa/packaging) module to parse and compare versions
 * Inspired by [piprot](https://github.com/sesh/piprot)

## Install

```bash
pip install git+https://github.com/Leryan/pyrrot
```

## Usage

```bash
pyrrot -r requirements.txt [--json]
```

## Example

### Default "human" output

```
$ pyrrot -r ~/someproject/requirements.txt > /dev/null
Beaker: old: wants: <1.6.0, latest: 1.9.0
influxdb: old: wants: ==2.12.0, latest: 5.0.0
pymongo: old: wants: <2.9.0, latest: 3.6.1
python-ldap: old: wants: <3.0.0, latest: 3.0.0
```

### JSON output

```
$ pyrrot -r ~/someproject/requirements.txt --printer pyrrot.JSONPrinter | python -m json.tool
```

```json
{
    "psutil": {
        "old": false,
        "wants": "<5.5.0",
        "latest": "5.4.3"
    },
    "pymongo": {
        "old": true,
        "wants": "<2.9.0",
        "latest": "3.6.1"
    }
}
```

## Todo

 * [x] Support for custom remote dependency checker
 * [ ] Support remote dependencies from git or any other VCS