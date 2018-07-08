import requests

from packaging.version import Version

class Remote(object):

    def __init__(self, location):
        super(Remote, self).__init__()
        self.location = location

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
                raise TypeError(
                    'get_latest_of returned a {} object instead of Version'.format(
                        version.__class__.__name__
                    )
                )

            latests[depname] = version

        return latests

class PyPi(Remote):
    """
    If you have another remote able to speak pypi.org's JSON api,
    subclass, override __init__ to super() then self.api_url = 'your_remote'.
    """

    def __init__(self, location):
        super(PyPi, self).__init__(location)

        self.s = requests.Session()
        self.api_url = '{}/{}/json'.format(self.location, '{}')

    def get_latest_of(self, name):
        r = self.s.get(self.api_url.format(name))

        if not r.ok:
            raise Exception(
                'dep {}: {}: {}'.format(name, r.status_code, r.text)
            )

        jr = r.json()

        return Version(jr['info']['version'])
