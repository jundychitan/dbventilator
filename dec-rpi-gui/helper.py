import datetime
from pyqtgraph import *
from os.path import realpath, abspath, dirname, join
import sys

"""
    Get environment setting
"""
def env(parameter, entry=False):
    if entry:
        parameter = "ENTRY_"+parameter
    
    with open(join(abspath(dirname(realpath(__file__))),'config.env'), 'r') as env_file:
        environment_array = env_file.read().split("\n")
        for param in environment_array:
            param = param.replace(" ", "")
            p_specific = param.split("=")[0]
            if p_specific==parameter:
                return join(abspath(dirname(realpath(__file__))),param.split("=")[1])

class TimeAxisItem(AxisItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setLabel(text='Time', units=None)
        self.enableAutoSIPrefix(False)

    def tickStrings(self, values, scale, spacing):
        return [datetime.datetime.fromtimestamp(value).strftime("%H:%M") for value in values]