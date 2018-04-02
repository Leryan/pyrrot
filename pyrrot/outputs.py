from sys import stdout, stderr

from json import JSONEncoder
from json import dumps as json_dumps

from packaging.version import Version


class Output(object):

    def print_olds(self, olds):
        raise NotImplementedError()


class Human(Output):

    def print_olds(self, olds):
        std_msg = '{}: {}: wants: {}, latest: {}\n'
        for req, val in olds.items():
            state = 'newest'
            old = val['old']
            if old:
                state = 'old'

            msg = std_msg.format(req, state, val['wants'], val['latest'])

            if old:
                stderr.write(msg)
            else:
                stdout.write(msg)

        stdout.flush()


class JSON(Output):

    def version_to_json(self, o):
        if isinstance(o, Version):
            return o.public

        return JSONEncoder.default(self, o)

    def print_olds(self, olds):
        stdout.write(json_dumps(olds, default=self.version_to_json))
        stdout.flush()
