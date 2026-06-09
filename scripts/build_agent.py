"""PyInstaller build for BiblioQ Agent (client bundle)."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
PYWIN32_RTH = SCRIPT_DIR / "pyi_rth_pywin32.py"

AGENT_HIDDEN = [
    "agent",
    "agent.commands",
    "agent.commands.handlers",
    "agent.config",
    "agent.machine",
]

SERVICE_HIDDEN = AGENT_HIDDEN + [
    "win32timezone",
    "pywintypes",
    "pythoncom",
    "win32api",
    "win32service",
    "win32serviceutil",
    "win32event",
    "servicemanager",
]


def _pyinstaller_cmd(
    name: str,
    entry: Path,
    output_dir: Path,
    *,
    hidden: list[str],
    collect_pywin32: bool = False,
    onefile: bool = True,
) -> list[str]:
    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--name",
        name,
        f"--paths={ROOT}",
        f"--distpath={output_dir}",
        f"--workpath={output_dir / '.pyi_build' / name}",
        f"--specpath={output_dir / '.pyi_build'}",
    ]
    if onefile:
        cmd.append("--onefile")
    else:
        cmd.append("--onedir")
    if collect_pywin32:
        cmd.extend(["--collect-all", "pywin32", f"--runtime-hook={PYWIN32_RTH}"])
    for mod in hidden:
        cmd.extend(["--hidden-import", mod])
    cmd.append(str(entry))
    return cmd


def _build(
    name: str,
    entry: Path,
    output_dir: Path,
    *,
    collect_pywin32: bool = False,
    onefile: bool = True,
) -> Path:
    hidden = SERVICE_HIDDEN if collect_pywin32 else AGENT_HIDDEN
    cmd = _pyinstaller_cmd(
        name,
        entry,
        output_dir,
        hidden=hidden,
        collect_pywin32=collect_pywin32,
        onefile=onefile,
    )
    subprocess.run(cmd, cwd=str(ROOT), check=True)
    if onefile:
        return output_dir / f"{name}.exe"
    return output_dir / name / f"{name}.exe"


def _flatten_service_onedir(output_dir: Path) -> Path:
    """Move onedir service output to agent/BiblioQAgentSvc.exe + agent/_internal/."""
    bundle_dir = output_dir / "BiblioQAgentSvc"
    exe_src = bundle_dir / "BiblioQAgentSvc.exe"
    internal_src = bundle_dir / "_internal"
    if not exe_src.is_file():
        raise RuntimeError(f"Service build missing executable: {exe_src}")
    if not internal_src.is_dir():
        raise RuntimeError(f"Service build missing _internal folder: {internal_src}")

    exe_dst = output_dir / "BiblioQAgentSvc.exe"
    internal_dst = output_dir / "_internal"

    if exe_dst.is_file():
        exe_dst.unlink()
    shutil.copy2(exe_src, exe_dst)

    if internal_dst.is_dir():
        shutil.rmtree(internal_dst)
    shutil.copytree(internal_src, internal_dst)

    shutil.rmtree(bundle_dir, ignore_errors=True)
    return exe_dst


def _assert_service_internal(output_dir: Path) -> None:
    internal = output_dir / "_internal"
    if not internal.is_dir():
        raise RuntimeError(f"Service _internal folder missing: {internal}")
    pywin_dir = internal / "pywin32_system32"
    dlls = list(pywin_dir.glob("pywintypes*.dll")) if pywin_dir.is_dir() else []
    if not dlls:
        raise RuntimeError(
            f"pywintypes DLL missing under {pywin_dir}. "
            "Rebuild with pywin32 installed: pip install pywin32>=306"
        )
    print(f"Verified service bundle: {internal} ({len(dlls)} pywin32 DLL(s))")


def _verify_service_exe(exe: Path) -> None:
    """Fail the build if pywin32 was not bundled into the service executable."""
    if not exe.is_file():
        raise RuntimeError(f"Service executable missing: {exe}")

    result = subprocess.run(
        [str(exe), "help"],
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )
    combined = f"{result.stdout or ''}\n{result.stderr or ''}"
    if "pywin32 required for windows service mode" in combined.lower():
        raise RuntimeError(
            f"{exe.name} is missing pywin32. Rebuild with pywin32 installed: "
            "pip install pywin32>=306"
        )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"{exe.name} smoke test failed (exit={result.returncode}): {combined[:400]}"
        )
    print(f"Verified {exe.name} loads pywin32")


def _verify_service_debug(exe: Path) -> None:
    """Run pywin32 debug mode briefly to confirm SvcDoRun can start."""
    proc = subprocess.Popen(
        [str(exe), "debug"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        time.sleep(3)
        if proc.poll() is not None:
            stdout = proc.stdout.read() if proc.stdout else b""
            stderr = proc.stderr.read() if proc.stderr else b""
            combined = (stdout + stderr).decode(errors="replace")
            if "pywin32 required for windows service mode" in combined.lower():
                raise RuntimeError(f"{exe.name} debug mode missing pywin32")
            raise RuntimeError(
                f"{exe.name} debug mode exited early (code={proc.returncode}): "
                f"{combined[:400]}"
            )
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print(f"Verified {exe.name} debug mode starts")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build BiblioQ agent executables")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist" / "BiblioQ" / "agent",
        help="Directory for BiblioQAgent.exe and BiblioQAgentSvc.exe",
    )
    parser.add_argument(
        "--skip-verify",
        action="store_true",
        help="Skip post-build pywin32 smoke test for BiblioQAgentSvc.exe",
    )
    args = parser.parse_args()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)

    if sys.platform != "win32":
        print("Warning: BiblioQAgentSvc requires Windows; building console agent only.")

    agent_exe = _build("BiblioQAgent", ROOT / "agent" / "agent.py", out)
    svc_exe = out / "BiblioQAgentSvc.exe"
    if sys.platform == "win32":
        _build(
            "BiblioQAgentSvc",
            ROOT / "agent" / "service_win.py",
            out,
            collect_pywin32=True,
            onefile=False,
        )
        svc_exe = _flatten_service_onedir(out)
        if not args.skip_verify:
            _assert_service_internal(out)
            _verify_service_exe(svc_exe)
            _verify_service_debug(svc_exe)

    example = ROOT / "agent" / "config.example.json"
    if example.is_file():
        shutil.copy2(example, out / "config.example.json")

    print(f"Built {agent_exe}")
    if sys.platform == "win32":
        print(f"Built {svc_exe}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
