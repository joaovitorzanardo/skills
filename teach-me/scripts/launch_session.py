#!/usr/bin/env python3
"""Open a new terminal running a fresh `claude` session, with the Course's HANDOFF.md as its first prompt.

  python3 launch_session.py <course-dir> [--dry-run]

The new session starts in the Course folder's parent (where the Topic was first taught).
Supported: WSL (Windows Terminal), macOS (Terminal.app), Linux desktops (x-terminal-emulator,
gnome-terminal, konsole, xterm). Anywhere else it prints a command for the Learner to run.

Exit codes: 0 = launched (or dry run), 1 = error, 3 = couldn't launch, command printed instead.
"""
import argparse
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HEADER = "TEACH-ME HANDOFF v"


def fail(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def is_wsl():
    if os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        return False


def terminal_command(script):
    """Return argv that opens a new terminal window running `bash -li <script>`, or None."""
    run = ["bash", "-li", script]
    if is_wsl() and shutil.which("wt.exe"):
        distro = os.environ.get("WSL_DISTRO_NAME")
        return ["wt.exe", "-w", "new", "wsl.exe"] + (["-d", distro] if distro else []) + ["--"] + run
    if sys.platform == "darwin" and shutil.which("osascript"):
        line = " ".join(shlex.quote(a) for a in run).replace("\\", "\\\\").replace('"', '\\"')
        return ["osascript", "-e", f'tell application "Terminal" to do script "{line}"',
                "-e", 'tell application "Terminal" to activate']
    if os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"):
        for term, flag in (("x-terminal-emulator", "-e"), ("gnome-terminal", "--"),
                           ("konsole", "-e"), ("xterm", "-e")):
            if shutil.which(term):
                return [term, flag] + run
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("course_dir")
    ap.add_argument("--dry-run", action="store_true", help="print what would run, launch nothing")
    args = ap.parse_args()

    course = Path(args.course_dir).expanduser().resolve()
    handoff = course / "HANDOFF.md"
    if not handoff.is_file():
        fail(f"{handoff} not found; write the handoff first")
    if not handoff.read_text(encoding="utf-8").lstrip().startswith(HEADER):
        fail(f"{handoff} must start with '{HEADER}1'")

    workdir = course.parent
    shell_line = f"cd {shlex.quote(str(workdir))} && claude \"$(cat {shlex.quote(str(handoff))})\""

    # A launcher script keeps the quoting out of the terminal's own argument parsing
    # (Windows Terminal, for one, treats ';' as a separator).
    fd, script = tempfile.mkstemp(prefix="teach-me-handoff-", suffix=".sh")
    with os.fdopen(fd, "w") as f:
        f.write(f"#!/usr/bin/env bash\nrm -f {shlex.quote(script)}\n{shell_line}\nexec bash\n")

    argv = terminal_command(script)
    if args.dry_run:
        os.remove(script)
        print("would run:", " ".join(shlex.quote(a) for a in argv) if argv else "(no terminal found)")
        print("session command:", shell_line)
        return
    if argv:
        try:
            subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL, start_new_session=True)
            print(f"launched a new session in {workdir}")
            return
        except OSError as e:
            print(f"launch failed: {e}")
    os.remove(script)
    print("Couldn't open a new terminal. Run this in one:")
    print(shell_line)
    sys.exit(3)


if __name__ == "__main__":
    main()
