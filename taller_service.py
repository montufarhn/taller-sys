import os
import sys
import threading
from datetime import datetime
from pathlib import Path

import win32event
import win32service
import win32serviceutil
import uvicorn

import main

SERVICE_NAME = "TallerProAutoService"
SERVICE_DISPLAY_NAME = "Taller Pro Auto Service"
SERVICE_DESCRIPTION = "Servicio Windows que ejecuta el servidor de Taller Pro Auto."


def write_log(message: str):
    base_dir = Path(__file__).resolve().parent
    log_path = base_dir / "taller_service.log"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass


class TallerProAutoService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME
    _svc_description_ = SERVICE_DESCRIPTION

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.server = None
        self.thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        if self.server is not None:
            self.server.should_exit = True
        win32event.SetEvent(self.stop_event)
        if self.thread is not None and self.thread.is_alive():
            self.thread.join(timeout=10)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        try:
            base_dir = Path(__file__).resolve().parent
            os.chdir(base_dir)

            self.ReportServiceStatus(win32service.SERVICE_START_PENDING)

            self.thread = threading.Thread(target=self.run_uvicorn, daemon=True)
            self.thread.start()

            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            write_log("Servicio iniciado correctamente.")
        except Exception as exc:
            write_log(f"SvcDoRun excepción: {exc}")
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            return

        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)

    def run_uvicorn(self):
        try:
            config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, log_level="info")
            self.server = uvicorn.Server(config)
            self.server.run()
        except Exception as exc:
            write_log(f"run_uvicorn excepción: {exc}")
            try:
                self.ReportServiceStatus(win32service.SERVICE_STOPPED)
            except Exception:
                pass
            win32event.SetEvent(self.stop_event)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(TallerProAutoService)
