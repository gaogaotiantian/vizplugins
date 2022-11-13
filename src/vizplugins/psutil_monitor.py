# licensed under the apache license: http://www.apache.org/licenses/license-2.0
# for details: https://github.com/gaogaotiantian/vizplugins/blob/master/notice.txt

import multiprocessing as mp
import os
from viztracer.vizplugin import VizPluginBase
from .monitor_process import MonitorProcess


class PsutilMonitor(VizPluginBase):
    def __init__(self, options, interval):
        super().__init__()
        self.action_queue = mp.Queue()
        self.data_queue = mp.Queue()
        self.options = options
        self.interval = interval
        self.recordings = []

    def support_version(self):
        return "0.15.6"

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
        self.cpu_process = mp.Process(target=MonitorProcess(self.action_queue, self.data_queue, self.options, self.interval),
                                      daemon=True)
        self.cpu_process.start()
        return {}

    def start_recording(self):
        return self.send_action("start")

    def stop_recording(self):
        self.recordings.append(self.send_action("stop"))
        return {}

    def save_data(self):
        self.recordings.append(self.send_action("get-data"))
        return {"action": "handle_data", "handler": self.append_data}

    def append_data(self, data):
        pid = os.getpid()
        assert isinstance(data, dict)
        for recording in self.recordings:
            for k in recording.keys():
                for data_point in recording[k]:
                    d = {"name": k,
                         "ph": "C",
                         "ts": data_point["ts"] * (1e6),
                         "args": data_point["arg"],
                         "pid": pid,
                         "tid": pid}
                    data["traceEvents"].append(d)
        self.recordings = []

    def terminate(self):
        self.send_action("terminate")
        self.cpu_process.join()
        return {"success": True}

    def send_action(self, message):
        if not self.cpu_process.is_alive():
            return {}
        self.action_queue.put(message)
        return self.data_queue.get()
