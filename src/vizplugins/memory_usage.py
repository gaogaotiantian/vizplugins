# licensed under the apache license: http://www.apache.org/licenses/license-2.0
# for details: https://github.com/gaogaotiantian/vizplugins/blob/master/notice.txt

import argparse
from .psutil_monitor import PsutilMonitor


def get_vizplugin(arg):
    parser = argparse.ArgumentParser(prog="vizplugins.memory_usage")
    parser.add_argument("-f", help="The frequency of sampling cpu usage", default=50)
    inputs = parser.parse_args(arg.split()[1:])
    options = {"memory_usage": True}
    interval = 1 / float(inputs.f)
    return PsutilMonitor(options, interval)
