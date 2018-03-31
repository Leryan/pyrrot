import argparse
import re
import sys

import json
from json import JSONEncoder

import requests

from packaging.requirements import Requirement
from packaging.version import Version
from packaging.specifiers import Specifier

class Remote(object):

    def get_dependency(self, name):
        """
        :rtype Version:
        """
        raise NotImplementedError()

class RemotePyPi(Remote):

    def __init__(self):
        super(RemotePyPi, self).__init__()

        self.s = requests.Session()
        self.api_url = 'https://pypi.python.org/pypi/{}/json'

    def get_dependency(self, name):
        r = self.s.get(self.api_url.format(name))

        if not r.ok:
            raise Exception(
                'dep {}: {}: {}'.format(name, r.status_code, r.text)
            )

        jr = r.json()

        return Version(jr['info']['version'])

class RemoteBullshit(Remote):

    def get_dependency(self, name):
        return Version('1.2.3')

class Printer(object):

    def print_olds(self, olds):
        raise NotImplementedError()

class HumanPrinter(Printer):

    def print_olds(self, olds):
        std_msg = '{}: {}: wants: {}, latest: {}\n'
        for req, val in olds.items():
            state = 'newest'
            old = val['old']
            if old:
                state = 'old'

            msg = std_msg.format(req, state, val['wants'], val['latest'])

            if old:
                sys.stderr.write(msg)
            else:
                sys.stdout.write(msg)

class JSONPrinter(Printer):

    def version_to_json(self, o):
        if isinstance(o, Version):
            return o.public

        return JSONEncoder.default(self, o)

    def print_olds(self, olds):
        print(json.dumps(olds, default=self.version_to_json))

class Pyrrot(object):

    def __init__(self, remote):
        if not issubclass(remote.__class__, Remote):
            raise TypeError('remote does not subclasses {}'.format(Remote.__class__.__name__))

        self.remote = remote

    def is_old(self, latest, specifiers):
        """
        :param latest Version:
        :param required SpecifierSet:
        """

        old = False

        for spec in specifiers:
            if spec.operator in ['>', '>=']:
                continue

            latest_spec = Specifier('<{}'.format(str(latest)))

            if list(latest_spec.filter([spec.version])):
                old = True

        return old

    def read_requirements(self, path):
        res = []

        with open(path, 'r') as fh:
            res = map(str.strip, fh.readlines())

        return res

    def parse_requirements(self, sreqs):
        """
        :param sreqs list[str]:
        """
        return {
            req.name: req.specifier for req in [
                Requirement(sreq) for sreq in sreqs
            ]
        }

    def get_latests(self, parsed):
        latests = {}

        for depname, _ in parsed.items():
            version = self.remote.get_dependency(depname)

            if not isinstance(version, Version):
                raise TypeError('remote.get_dependency returned a {} object instead of Version'.format(version.__class__.__name__))

            latests[depname] = version

        return latests

    def get_olds(self, parsed, latests):
        olds = {}

        for req, vreq in parsed.items():
            olds[req] = {
                'old': self.is_old(latests[req], vreq),
                'wants': str(parsed[req]),
                'latest': latests[req]
            }

        return olds

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', help='requirements.txt file', required=True, dest='reqs')
        parser.add_argument('--json', action='store_true', help='print as json')

        args = parser.parse_args()

        reqs = self.read_requirements(args.reqs)
        parsed = self.parse_requirements(reqs)
        latests = self.get_latests(parsed)
        olds = self.get_olds(parsed, latests)

        if args.json:
            printer = JSONPrinter()
        else:
            printer = HumanPrinter()

        printer.print_olds(olds)


    @staticmethod
    def App():
        remote = RemotePyPi()
        #remote = RemoteBullshit()
        return Pyrrot(remote)

def main():
    app = Pyrrot.App()
    app.run()
