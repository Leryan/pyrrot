import argparse
import json
import re

import requests

from packaging import version

class Printer(object):

    def print_olds(self, olds):
        raise NotImplementedError()

class HumanPrinter(Printer):

    def print_olds(self, olds):
        for req, val in olds.items():
            if val['old'] is True:
                print('{}: wants: {}, latest is {}'.format(
                    req, val['wants'], val['latest']
                ))

class JSONPrinter(Printer):

    def print_olds(self, olds):
        print(json.dumps(olds))

class Pyrrot(object):

    RE_VERSION_CHECK = re.compile('^([^<=>]+)(<|<=|==|>=|>)([^<=>]+)$')

    def __init__(self):
        self.s = requests.Session()

    def compare(self, current, operator, latest):
        vcurrent = version.parse(current)
        vlatest = version.parse(latest)

        if operator == '<':
            return vcurrent < vlatest

        elif operator == '<=':
            return vcurrent <= vlatest

        elif operator == '==':
            return vcurrent == vlatest

        elif operator == '>=':
            return vcurrent >= vlatest

        elif operator == '>':
            return vcurrent > vlatest

        raise ValueError('unsupported operator "{}"'.format(operator))

    def check_constraint(self, current, constraint, latest):
        return self.compare(latest, constraint, current)

    def read_requirements(self, path):
        res = []

        with open(path, 'r') as fh:
            res = map(str.strip, fh.readlines())

        return res

    def parse_requirements(self, reqs):
        """
        :param reqs list[str]:
        """
        parsed = {}

        for req in reqs:
            m = self.RE_VERSION_CHECK.match(req)
            if m is not None:
                depname = m.group(1)
                depoperator = m.group(2)
                depversion = m.group(3)
                parsed[depname] = {
                    'operator': depoperator,
                    'version': depversion
                }

        return parsed

    def get_latest(self, depname):
        r = self.s.get('https://pypi.python.org/pypi/{}/json'.format(
            depname
        ))

        if not r.ok:
            raise Exception('dep {}: {}: {}'.format(depname, r.status_code, r.text))

        jr = r.json()

        return jr['info']['version']

    def get_latests(self, parsed):
        latests = {}

        for depname, _ in parsed.items():
            latests[depname] = self.get_latest(depname)

        return latests

    def get_olds(self, parsed, latests):
        olds = {}

        for req, vreq in parsed.items():
            is_old = not self.check_constraint(
                vreq['version'], vreq['operator'], latests[req]
            )

            olds[req] = {
                'old': is_old,
                'wants': '{}{}'.format(vreq['operator'], vreq['version']),
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
        return Pyrrot()

def main():
    app = Pyrrot.App()
    app.run()