"""PyInstaller runtime hook: ensure pywin32 DLLs load from the bundle."""

import os
import sys

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    meipass = sys._MEIPASS
    os.environ["PATH"] = meipass + os.pathsep + os.environ.get("PATH", "")
