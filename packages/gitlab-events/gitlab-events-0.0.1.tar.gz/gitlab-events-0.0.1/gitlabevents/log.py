import colorama
from termcolor import colored


class Logger(object):
    log_table = {
        "info"    : colored('[*]', 'blue', attrs=['bold']),
        "warn"    : colored('[!]', 'yellow', attrs=['bold']),
        "failure" : colored('[-]', 'red', attrs=['bold']),
    }

    def __init__(self, logger=None):
        colorama.init()

    def info(self, message):
        print(log_table['info'] + message)

    def warn(self, message):
        print(log_table['warn'] + message)

    def failure(self, message):
        print(log_table['failure'] + message)


