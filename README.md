# Pyrrot

Python Rotten Requirements

 * Supports `pypi.python.org` as remote repository by default
 * Supports "human" and JSON output
 * Uses the [packaging](https://github.com/pypa/packaging) module to parse and compare versions
 * Inspired by [piprot](https://github.com/sesh/piprot)

## Install

```bash
pip install git+https://github.com/Leryan/pyrrot
```

## Usage

```bash
pyrrot -r requirements.txt [--remote package.RemoteClass] [--printer package.PrinterClass]
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

## Hack it

### Custom remote for latest versions

Create your own subclass of `pyrrot.Remote` and use it with `--remote yourpackage.YourRemote`. See `pyrrot.RemotePyPi` for an example.

### Custom output

See `pyrrot.HumanPrinter` class. Create your own subclass of `pyrrot.Printer` and use it with `--printer yourpackage.YourPrinter`.

Of course "printer" here doesn't mean you have to output on `stdout`, you could for example put results in a database.

## Todo

 * [x] Support for custom remote dependency checker
 * [ ] Check requirements for currently installed package
 * [ ] Support remote dependencies from git or any other VCS
