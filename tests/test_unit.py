from .base_tmpl import BaseTmpl
from vizplugins.cpu_time import PsutilCpuPercentage, MonitorCPU
import multiprocessing as mp


class TestBasics(BaseTmpl):
    def test_message(self):
        cpu = PsutilCpuPercentage("")
        self.assertDictEqual(cpu.message("dummy", {}), {})

    def test_process_state(self):
        action = mp.Queue()
        data = mp.Queue()
        p = MonitorCPU(action, data, 0.05)
        action.put("get-data")
        action.put("terminate")
        p.state = "running"
        p()
        self.assertEqual(p.state, "stopped")
