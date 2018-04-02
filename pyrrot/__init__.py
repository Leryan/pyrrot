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

from pyrrot.utils import get_class

__version__ = '0.0.4'

class ReqReader(object):

    def __init__(self, location):
        self.location = location

    def read(self):
        """
        Override this method and use self.location

        :returns: requirements as they would be written in a requirements.txt file
        :rtype list[str]:
        """
        raise NotImplementedError()


class ReqReaderFile(ReqReader):

    def read(self):
        res = []

        with open(self.location, 'r') as fh:
            res = map(str.strip, fh.readlines())

        return res

class Remote(object):

    def get_latest_of(self, name):
        """
        :rtype Version:
        """
        raise NotImplementedError()

    def get_latests(self, dependencies):
        """
        You may want to override this method if you are able
        to fetch all dependencies at once and build the map
        is required.

        Otherwise, this function will ask get_latest_of() to work.

        :param dependencies list[str]: dependencies name
        :returns: map of dependencies latest version
        :rtype dict[str]Version
        """
        latests = {}

        for depname in dependencies:
            version = self.get_latest_of(depname)

            if not isinstance(version, Version):
                raise TypeError('get_latest_of returned a {} object instead of Version'.format(version.__class__.__name__))

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

    def get_latest_of(self, name):
        r = self.s.get(self.api_url.format(name))

        if not r.ok:
            raise Exception(
                'dep {}: {}: {}'.format(name, r.status_code, r.text)
            )

        jr = r.json()

        return Version(jr['info']['version'])

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
    def parse_requirements(sreqs):
        """
        :param sreqs list[str]:
        """
        return {
            req.name: req.specifier for req in [
                Requirement(sreq) for sreq in sreqs
            ]
        }

    def get_olds(self, parsed, latests):
        olds = {}

        for req, vreq in parsed.items():
            olds[req] = {
                'old': self.is_old(latests[req], vreq),
                'wants': str(parsed[req]),
                'latest': latests[req]
            }

        return olds

    def work(self, reqreader, remote, printer):
        """
        :param reqreader ReqReader:
        :param remote Remote:
        :param printer Printer:
        """
        reqs = reqreader.read()
        parsed = self.parse_requirements(reqs)
        latests = remote.get_latests(parsed.keys())
        olds = self.get_olds(parsed, latests)
        printer.print_olds(olds)

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', help='requirements.txt file location', required=True, dest='reqs')
        parser.add_argument(
            '--printer',
            default='{}.HumanPrinter'.format(__name__),
            help='output class. for JSON use {}.JSONPrinter'.format(__name__)
        )
        parser.add_argument('--reqreader', default='{}.ReqReaderFile'.format(__name__))
        parser.add_argument('--remote', default='{}.RemotePyPi'.format(__name__))

        args = parser.parse_args()

        remote_class = get_class(args.remote, Remote)
        printer_class = get_class(args.printer, Printer)
        reqreader_class = get_class(args.reqreader, ReqReader)

        printer = printer_class()
        remote = remote_class()
        reqreader = reqreader_class(args.reqs)

        self.work(reqreader, remote, printer)


    @staticmethod
    def App():
        return Pyrrot()

def main():
    app = Pyrrot.App()
    app.run()
