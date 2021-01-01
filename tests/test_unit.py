from .base_tmpl import BaseTmpl
from vizplugins.cpu_usage import PsutilCpuPercentage, MonitorCPU
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
        action.close()
        action.join_thread()
        self.assertEqual(p.state, "stopped")

    def test_frequency_option(self):
        c1 = PsutilCpuPercentage("vizplugins.cpu_usage")
        self.assertEqual(c1.interval, 0.02)
        c2 = PsutilCpuPercentage("vizplugins.cpu_usage -f 20")
        self.assertAlmostEqual(c2.interval, 0.05)
