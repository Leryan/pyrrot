import argparse

from packaging.requirements import Requirement
from packaging.specifiers import Specifier, SpecifierSet
from packaging.version import Version

from pyrrot.outputs import Output
from pyrrot.remotes import Remote
from pyrrot.reqreaders import ReqReader
from pyrrot.utils import get_class


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

    def work(self, reqreader, remote, output):
        """
        :param reqreader ReqReader:
        :param remote Remote:
        :param output Output:
        """
        reqs = reqreader.read()
        parsed = self.parse_requirements(reqs)
        latests = remote.get_latests(parsed.keys())
        olds = self.get_olds(parsed, latests)
        output.print_olds(olds)

    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-r', help='requirements location', required=True, dest='reqs')
        parser.add_argument(
            '--output',
            default='{}.outputs.Human'.format(__name__),
            help='output class. for JSON use {}.outputs.JSON'.format(__name__)
        )
        parser.add_argument('--reqreader', default='{}.reqreaders.File'.format(__name__))
        parser.add_argument('--remote', default='{}.remotes.PyPi'.format(__name__))
        parser.add_argument('--remote-location', default='https://pypi.org/pypi')

        args = parser.parse_args()

        reqreader_class = get_class(args.reqreader, ReqReader)
        remote_class = get_class(args.remote, Remote)
        output_class = get_class(args.output, Output)

        reqreader = reqreader_class(args.reqs)
        remote = remote_class(args.remote_location)
        output = output_class()

        self.work(reqreader, remote, output)


    @staticmethod
    def App():
        return Pyrrot()

def main():
    Pyrrot.App().run()
