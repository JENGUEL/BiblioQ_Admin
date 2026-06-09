"""Windows service wrapper for BiblioQ agent."""

import os
import sys
import threading

try:
    import servicemanager
    import win32event
    import win32service
    import win32serviceutil
except ImportError:
    print("pywin32 required for Windows service mode.")
    sys.exit(1)

if getattr(sys, "frozen", False):
    _ROOT = os.path.dirname(sys.executable)
else:
    _ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# BiblioQ_Admin root for package imports when frozen onefile extracts elsewhere
_admin_root = os.path.dirname(_ROOT) if os.path.basename(_ROOT).lower() == "agent" else _ROOT
_biblioq_admin = _admin_root if os.path.isdir(os.path.join(_admin_root, "agent")) else os.path.dirname(_admin_root)
if _biblioq_admin not in sys.path:
    sys.path.insert(0, _biblioq_admin)


class BiblioQAgentService(win32serviceutil.ServiceFramework):
    _svc_name_ = "BiblioQAgent"
    _svc_display_name_ = "BiblioQ Remote Agent"
    _svc_description_ = "Polls BiblioQ Admin for telemetry and remote commands."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        self.running = False

    def SvcDoRun(self):
        # Windows SCM times out if SERVICE_RUNNING is not reported quickly (~30s).
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogMsg(
            servicemanager.EVENTLOG_INFORMATION_TYPE,
            servicemanager.PYS_SERVICE_STARTED,
            (self._svc_name_, ""),
        )
        worker = threading.Thread(target=self._run_agent, name="BiblioQAgent", daemon=True)
        worker.start()
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def _run_agent(self) -> None:
        try:
            from agent.agent import main_loop

            main_loop()
        except Exception as ex:
            servicemanager.LogErrorMsg(f"BiblioQ agent loop failed: {ex}")


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(BiblioQAgentService)
