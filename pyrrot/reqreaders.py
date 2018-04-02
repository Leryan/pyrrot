class ReqReader(object):

    def __init__(self, location):
        super(ReqReader, self).__init__()
        self.location = location

    def read(self):
        """
        Override this method and use self.location

        :returns: requirements as they would be written in a requirements.txt file
        :rtype list[str]:
        """
        raise NotImplementedError()


class File(ReqReader):

    def read(self):
        res = []

        with open(self.location, 'r') as fh:
            res = map(str.strip, fh.readlines())

        return res
