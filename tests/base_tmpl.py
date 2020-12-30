# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://github.com/gaogaotiantian/vizplugin/blob/master/NOTICE.txt

from unittest import TestCase
import gc


class BaseTmpl(TestCase):
    def setUp(self):
        print("{} start".format(self.id()))

    def tearDown(self):
        print("{} finish".format(self.id()))
        gc.collect()

    def assertEventNumber(self, data, expected_entries):
        entries = len([1 for entry in data["traceEvents"] if entry["ph"] != "M"])
        self.assertEqual(entries, expected_entries)
