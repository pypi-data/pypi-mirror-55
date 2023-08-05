from typing import Dict


class ServerError(Exception):
    response: Dict = {}
    url: str = ""

    def __init__(self, message, response=None, url=None, **kw):
        self.response = response
        self.url = url
        self.message = message

    def __str__(self):
        ret = self.message
        if self.url:
            ret += " - {}".format(self.url)
        return ret


class InvalidToken(Exception):
    pass


class InvalidProfile(Exception):
    pass


class ServiceNotFound(Exception):
    pass
