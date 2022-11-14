# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/vizplugins/blob/master/NOTICE.txt

from .cpu_usage import PsutilMonitor
import argparse


__version__ = "0.1.3"


def get_vizplugin(arg):
    parser = argparse.ArgumentParser(prog="vizplugins")
    parser.add_argument("-f", help="The frequency of sampling cpu usage", default=50)
    parser.add_argument("--cpu_usage", action="store_true")
    parser.add_argument("--memory_usage", action="store_true")
    inputs = parser.parse_args(arg.split()[1:])
    options = {}
    if inputs.cpu_usage:
        options["cpu_usage"] = True
    if inputs.memory_usage:
        options["memory_usage"] = True
    interval = 1 / float(inputs.f)
    return PsutilMonitor(options, interval)
