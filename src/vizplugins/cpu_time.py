# licensed under the apache license: http://www.apache.org/licenses/license-2.0
# for details: https://github.com/gaogaotiantian/vizplugins/blob/master/notice.txt

import multiprocessing as mp
import psutil
import os
import time
from viztracer.vizplugin import VizPluginBase


def get_vizplugin(arg):
    return PsutilCpuPercentage(arg)


class PsutilCpuPercentage(VizPluginBase):
    def __init__(self, arg):
        super().__init__()
        self.actions = mp.Queue()
        self.data = mp.Queue()
        self.interval = 0.02

    def message(self, m_type, payload):
        if m_type == "event":
            if payload["when"] == "initialize":
                return self.generate_process()
            elif payload["when"] == "post-stop":
                print("post-stop")
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
        self.cpu_process = mp.Process(target=MonitorCPU(self.actions, self.data, self.interval), daemon=True)
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
        for ts, cpu_percent in self.recording["data"]:
            d = {"name": "cpu_percentage",
                 "ph": "C",
                 "ts": ts * (1e6),
                 "args": {"cpu_percent": cpu_percent},
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


class MonitorCPU:
    def __init__(self, actions, data, interval):
        self.actions = actions
        self.data = data
        self.interval = interval
        self.state = "stopped"

    def __call__(self):
        p = psutil.Process(os.getppid())
        p.cpu_percent()
        cpu_percent = []
        times = []
        while True:
            data = {}
            if not self.actions.empty():
                action = self.actions.get()
                if action == "start":
                    self.state = "running"
                    times.append(time.monotonic())
                elif action == "stop":
                    self.state = "stopped"
                    # to indicate the end of recording(otherwise the last data point will not be shown)
                    cpu_percent.append(0)
                elif action == "get-data":
                    if self.state != "stopped":
                        self.state = "stopped"
                        cpu_percent.append(0)
                    data["data"] = list(zip(times, cpu_percent))
                    cpu_percent = []
                    times = []
                elif action == "terminate":
                    break
                self.data.put(data)
            time.sleep(self.interval)
            if self.state == "running":
                cpu_percent.append(p.cpu_percent())
                times.append(time.monotonic())
        self.data.put({})
