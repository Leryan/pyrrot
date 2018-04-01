import argparse
import importlib
import re
import sys

import json
from json import JSONEncoder

import requests

from packaging.requirements import Requirement
from packaging.version import Version
from packaging.specifiers import Specifier, SpecifierSet

class Remote(object):

    def get_dependency(self, name):
        """
        :rtype Version:
        """
        raise NotImplementedError()

    def get_latests(self, dependencies):
        """
        You may want to override this method if you are able
        to fetch all dependencies at once and build the map
        is required.

        Otherwise, this function will ask get_dependency() to work.

        :param dependencies list[str]: dependencies name
        :returns: map of dependencies latest version
        :rtype dict[str]Version
        """
        latests = {}

        for depname in dependencies:
            version = self.get_dependency(depname)

            if not isinstance(version, Version):
                raise TypeError('get_dependency returned a {} object instead of Version'.format(version.__class__.__name__))

            latests[depname] = version

        return latests

class RemotePyPi(Remote):
    """
    If you have another remote able to speak pypi.python.org's JSON api,
    subclass, override __init__ to super() then self.api_url = 'your_remote'.
    """

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

    @staticmethod
    def is_old(latest, specifiers):
        """
        :param latest Version:
        :param required SpecifierSet:
        """

        if not isinstance(latest, Version):
            raise TypeError('latest is not of type Version')

        if not isinstance(specifiers, SpecifierSet):
            raise TypeError('specifiers is not of type SpecifierSet')

        old = False

        for spec in specifiers:
            if spec.operator in ['>', '>=']:
                continue

            latest_op = '<'
            if spec.operator in ['<']:
                latest_op = '<='

            latest_spec = Specifier('{}{}'.format(
                latest_op,
                str(latest)
            ))

            if list(latest_spec.filter([spec.version])):
                old = True

        return old

    @staticmethod
    def read_requirements(path):
        res = []

        with open(path, 'r') as fh:
            res = map(str.strip, fh.readlines())

        return res

    @staticmethod
    def parse_requirements(sreqs):
        """
        :param sreqs list[str]:
        """
        return {
            req.name: req.specifier for req in [
                Requirement(sreq) for sreq in sreqs
            ]
        }

    @classmethod
    def get_class(cls, mod_path):
        mp = mod_path.split('.')

        mod_path = '.'.join(mp[:-1])
        class_name = mp[-1]

        module = importlib.import_module(mod_path)

        the_class = getattr(module, class_name, None)

        if the_class is None:
            raise Exception('remote class not found: {}'.format(mod_path))

        return the_class

    @classmethod
    def get_remote_class(cls, remote_mod_path):
        remote_class = cls.get_class(remote_mod_path)

        if not issubclass(remote_class, Remote):
            raise TypeError('remote does not subclasses {}'.format(Remote.__name__))

        return remote_class

    @classmethod
    def get_printer_class(cls, printer_mod_path):
        printer_class = cls.get_class(printer_mod_path)

        if not issubclass(printer_class, Printer):
            raise TypeError('remote does not subclasses {}'.format(Printer.__name__))

        return printer_class

    def get_olds(self, parsed, latests):
        olds = {}

        for req, vreq in parsed.items():
            olds[req] = {
                'old': self.is_old(latests[req], vreq),
                'wants': str(parsed[req]),
                'latest': latests[req]
            }

        return olds

    def work(self, requirements_path, remote):
        reqs = self.read_requirements(requirements_path)
        parsed = self.parse_requirements(reqs)
        latests = remote.get_latests(parsed.keys())
        olds = self.get_olds(parsed, latests)

        return olds

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', help='requirements.txt file', required=True, dest='reqs')
        parser.add_argument(
            '--printer',
            default='{}.HumanPrinter'.format(__name__),
            help='output class. for JSON use {}.JSONPrinter'.format(__name__)
        )
        parser.add_argument('--remote', default='{}.RemotePyPi'.format(__name__))

        args = parser.parse_args()

        remote_class = self.get_remote_class(args.remote)
        printer_class = self.get_printer_class(args.printer)

        printer = printer_class()
        remote = remote_class()
        olds = self.work(args.reqs, remote)

        printer.print_olds(olds)


    @staticmethod
    def App():
        return Pyrrot()

def main():
    app = Pyrrot.App()
    app.run()
