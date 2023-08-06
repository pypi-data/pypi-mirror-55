import requests
from ..helpers import trace
import logging

logging.addLevelName(logging.DEBUG + 5, "VERBOSE")
logger = logging.getLogger('lumber')

def init(token):
    return Lumber(token)

class Lumber:

    url = 'https://api.lumber.cloud/logs'

    def __init__(self, token, options={}):
        self.token = 'Bearer ' + token
        self.local = False if 'local' in options and not options.local else True
        self.cloud = False if 'cloud' in options and not options.cloud else True

    def log(self, message, code=None, level=0):
        if level == 1:
            logger.debug(u'\x1b[34m{}\x1b[39m'.format(message))
        elif level == 2:
            logger.log(logging.DEBUG + 5, message)
        elif level == 3:
            logger.warning(u'\x1b[33m{}\x1b[39m'.format(message))
        elif level == 4:
            logger.error(u'\x1b[31m{}\x1b[39m'.format(message))
        elif level == 5:
            logger.critical(u'\x1b[38;5;208m{}\x1b[39m'.format(message))
        else:
            logger.info(message)

    def logCloud(self, message, code=None, level=0):
        t = trace()
        payload = {
            'code': code,
            'level': level,
            'message': message,
            'line': t['line'],
            'method': t['method']
        }
        headers = {'Authorization': self.token}
        response = requests.post(Lumber.url, json=payload, headers=headers)
        return response

    def info(self, message, code=None):
        if (self.local): self.log(message, code)
        return self.logCloud(message, code)

    def debug(self, message, code=None):
        if (self.local): self.log(message, code, 1)
        return self.logCloud(message, code, 1)

    def verbose(self, message, code=None):
        if (self.local): self.log(message, code, 2)
        return self.logCloud(message, code, 2)

    def warning(self, message, code=None):
        if (self.local): self.log(message, code, 3)
        return self.logCloud(message, code, 3)

    def error(self, message, code=None):
        if (self.local): self.log(message, code, 4)
        return self.logCloud(message, code, 4)

    def critical(self, message, code=None):
        if (self.local): self.log(message, code, 5)
        return self.logCloud(message, code, 5)
