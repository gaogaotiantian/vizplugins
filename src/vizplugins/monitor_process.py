# licensed under the apache license: http://www.apache.org/licenses/license-2.0
# for details: https://github.com/gaogaotiantian/vizplugins/blob/master/notice.txt

import psutil
import os
import time


class MonitorProcess:
    def __init__(self, actions, data, options, interval):
        self.actions = actions
        self.data = data
        self.interval = interval
        self.options = options
        self.state = "stopped"
        self.parent = None
        self.record_handlers = {"cpu_usage": self.cpu_usage_handler,
                                "memory_usage": self.memory_usage_handler}
        self.pack_handlers = {"cpu_usage": self.cpu_usage_pack,
                              "memory_usage": self.memory_usage_pack}
        self.recordings = {}
        self.init_recording()

    def __call__(self):
        self.parent = psutil.Process(os.getppid())
        if "cpu_usage" in self.options:
            self.parent.cpu_percent()
        while True:
            data = {}
            if not self.actions.empty():
                action = self.actions.get()
                if action == "start":
                    self.state = "running"
                    self.recordings["ts"].append(time.monotonic())
                elif action == "stop":
                    self.state = "stopped"
                    # to indicate the end of recording(otherwise the last data point will not be shown)
                    self.record_data()
                    # Every time we get a stop, record the data and send it back
                    # because we may never get the get-data command due to
                    # early process termination
                    data = self.pack_data()
                    self.init_recording()
                elif action == "get-data":
                    if self.state != "stopped":
                        self.state = "stopped"
                        self.record_data()
                    data = self.pack_data()
                    self.init_recording()
                elif action == "terminate":
                    break
                self.data.put(data)
            time.sleep(self.interval)
            if self.state == "running":
                self.record_data()
                self.recordings["ts"].append(time.monotonic())
        self.data.put({})

    def record_data(self):
        for k in self.options.keys():
            self.record_handlers[k]()

    def cpu_usage_handler(self):
        self.recordings["cpu_percent"].append(self.parent.cpu_percent())

    def memory_usage_handler(self):
        info = self.parent.memory_info()
        self.recordings["physical_memory"].append(info.rss)
        self.recordings["virtual_memory"].append(info.vms)

    def pack_data(self):
        data = {}
        for k in self.options.keys():
            data[k] = self.pack_handlers[k]()
        return data

    def cpu_usage_pack(self):
        zipped = []
        for i in range(len(self.recordings["ts"])):
            zipped.append({"ts": self.recordings["ts"][i],
                           "arg": {"cpu_percent": self.recordings["cpu_percent"][i]}})
        return zipped

    def memory_usage_pack(self):
        zipped = []
        for i in range(len(self.recordings["ts"])):
            zipped.append({"ts": self.recordings["ts"][i],
                           "arg": {"rss": self.recordings["physical_memory"][i],
                                   "vms": self.recordings["virtual_memory"][i]}})
        return zipped

    def init_recording(self):
        self.recordings = {"cpu_percent": [],
                           "physical_memory": [],
                           "virtual_memory": [],
                           "ts": []}
