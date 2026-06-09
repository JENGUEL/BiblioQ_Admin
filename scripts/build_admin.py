"""PyInstaller build for BiblioQ Admin."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name",
        "BiblioQ_Admin",
        str(ROOT / "main.py"),
    ]
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    print("Built dist/BiblioQ_Admin.exe")


if __name__ == "__main__":
    main()
