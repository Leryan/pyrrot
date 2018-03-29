# Pyrrot

Python Rotten Requirements

 * Supports **only** `pypi.python.org` as remote repository
 * Uses the `packaging` module to parse and compare versions
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
$ pyrrot -r ~/someproject/requirements.txt
Beaker: wants: <1.6.0, latest is 1.9.0
influxdb: wants: ==2.12.0, latest is 5.0.0
pymongo: wants: <2.9.0, latest is 3.6.1
python-ldap: wants: <3.0.0, latest is 3.0.0
```

### JSON output

```
$ pyrrot -r ~/someproject/requirements.txt --json | python -m json.tool
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

 * [ ] Support remote dependencies from git or any other VCS
 * [ ] Support for custom remote dependency checker