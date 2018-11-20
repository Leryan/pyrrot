# Pyrrot

Python Rotten Requirements

 * Supports any remote repository that speaks PyPi's `/json` API through the `--remote-location` parameter
 * Supports "human" and JSON output
 * Uses the [packaging](https://github.com/pypa/packaging) module to parse and compare versions
 * Inspired by [piprot](https://github.com/sesh/piprot)

## Install

```bash
pip install git+https://github.com/Leryan/pyrrot
```

## Usage

```bash
pyrrot -r requirements.txt [--reqreader package.ReqReaderClass] [--remote package.RemoteClass] [--output package.OutputClass]
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
$ pyrrot -r ~/someproject/requirements.txt --output pyrrot.remotes.JSON | python -m json.tool
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

Create your own subclass of `pyrrot.remotes.Remote` and use it with `--remote yourpackage.YourRemote`. See `pyrrot.remotes.PyPi` for an example.

### Custom output

See `pyrrot.outputs.Human` class. Create your own subclass of `pyrrot.outputs.Output` and use it with `--output yourpackage.YourOutput`.

This could allow you to put results in a database.

## Todo

 * [ ] Check requirements for currently installed package
 * [ ] Support remote dependencies from git or any other VCS
 * [ ] Support "pip options" like `-e` or `-r`
