from .base_tmpl import BaseTmpl
import vizplugins
import multiprocessing as mp


class TestBasics(BaseTmpl):
    def test_message(self):
        cpu = vizplugins.cpu_usage.PsutilMonitor({"cpu_usage": True}, 0.02)
        self.assertDictEqual(cpu.message("dummy", {}), {})

    def test_process_state(self):
        action = mp.Queue()
        data = mp.Queue()
        p = vizplugins.MonitorProcess.MonitorProcess(action, data, {"cpu_usage": True, "memory_usage": True}, 0.05)
        action.put("get-data")
        action.put("terminate")
        p.state = "running"
        p()
        action.close()
        action.join_thread()
        self.assertEqual(p.state, "stopped")

    def test_frequency_option(self):
        c1 = vizplugins.cpu_usage.get_vizplugin("vizplugins.cpu_usage")
        self.assertEqual(c1.interval, 0.02)
        c2 = vizplugins.cpu_usage.get_vizplugin("vizplugins.cpu_usage -f 20")
        self.assertAlmostEqual(c2.interval, 0.05)
        c2 = vizplugins.get_vizplugin("vizplugins --cpu_usage -f 20")
        self.assertAlmostEqual(c2.interval, 0.05)
