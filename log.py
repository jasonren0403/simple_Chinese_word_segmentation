import datetime
import sys


# log
class Logger(object):
    def __init__(self, fileN="Default.log"):
        self.terminal = sys.stdout
        self.log = open(fileN, "a+")

    def write(self, message):
        self.terminal.write(message)
        self.log.write("["+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")+"]")
        self.log.write(message)

    def flush(self):
        pass