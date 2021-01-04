# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/vizplugin/blob/master/NOTICE.txt

from .cmdline_tmpl import CmdlineTmpl


file_fib_long = """
def fib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)
fib(30)
"""

file_sleep = """
import time
time.sleep(1)
"""


class TestCommandLine(CmdlineTmpl):
    def test_cpu_exist(self):
        def check_func(data):
            counter = 0
            for entry in data["traceEvents"]:
                if entry["ph"] == "C" and entry["name"] == "cpu_usage":
                    counter += 1
            self.assertGreater(counter, 0)
        self.template(["viztracer", "--plugins", "vizplugins.cpu_usage", "-o", "result.json", "cmdline_test.py"],
                      script=file_sleep,
                      expected_output_file="result.json",
                      concurrency="multiprocessing",
                      check_func=check_func)

    def test_memory_exist(self):
        def check_func(data):
            counter = 0
            for entry in data["traceEvents"]:
                if entry["ph"] == "C" and entry["name"] == "memory_usage":
                    counter += 1
            self.assertGreater(counter, 0)
        self.template(["viztracer", "--plugins", "vizplugins --cpu_usage --memory_usage",
                       "-o", "result.json", "cmdline_test.py"],
                      script=file_sleep,
                      expected_output_file="result.json",
                      concurrency="multiprocessing",
                      check_func=check_func)
