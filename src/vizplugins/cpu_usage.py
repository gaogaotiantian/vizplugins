# licensed under the apache license: http://www.apache.org/licenses/license-2.0
# for details: https://github.com/gaogaotiantian/vizplugins/blob/master/notice.txt

import multiprocessing as mp
import os
import argparse
from viztracer.vizplugin import VizPluginBase
from .MonitorProcess import MonitorProcess


def get_vizplugin(arg):
    parser = argparse.ArgumentParser(prog="vizplugins.cpu_usage")
    parser.add_argument("-f", help="The frequency of sampling cpu usage")
    inputs = parser.parse_args(arg.split()[1:])
    options = {"cpu_usage": True}
    if inputs.f:
        return PsutilMonitor(options, 1 / float(inputs.f))
    else:
        return PsutilMonitor(options, 0.02)


class PsutilMonitor(VizPluginBase):
    def __init__(self, options, interval):
        super().__init__()
        self.actions = mp.Queue()
        self.data = mp.Queue()
        self.options = options
        self.interval = interval

    def support_version(self):
        return "0.11.0"

    def message(self, m_type, payload):
        if m_type == "event":
            if payload["when"] == "initialize":
                return self.generate_process()
            elif payload["when"] == "post-stop":
                return self.stop_recording()
            elif payload["when"] == "pre-save":
                return self.save_data()
            elif payload["when"] == "pre-start":
                return self.start_recording()
        elif m_type == "command":
            if payload["cmd_type"] == "terminate":
                return self.terminate()
        return {}

    def generate_process(self):
        self.cpu_process = mp.Process(target=MonitorProcess(self.actions, self.data, self.options, self.interval), daemon=True)
        self.cpu_process.start()
        return {}

    def start_recording(self):
        return self.send_action("start")

    def stop_recording(self):
        return self.send_action("stop")

    def save_data(self):
        self.recording = self.send_action("get-data")
        return {"action": "handle_data", "handler": self.append_data}

    def append_data(self, data):
        pid = os.getpid()
        for k in self.recording.keys():
            for data_point in self.recording[k]:
                d = {"name": k,
                     "ph": "C",
                     "ts": data_point["ts"] * (1e6),
                     "args": data_point["arg"],
                     "pid": pid,
                     "tid": pid}
                data["traceEvents"].append(d)

    def terminate(self):
        self.send_action("terminate")
        self.cpu_process.join()
        return {"success": True}

    def send_action(self, message):
        self.actions.put(message)
        return self.data.get()
