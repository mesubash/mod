"""Shared pipeline constants and helpers."""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def pdf_text(path):
    return subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True, text=True, check=True).stdout


def sumo_tool(name):
    """Path to a working SUMO binary.

    The eclipse-sumo wheel ships binaries that need system libraries a headless
    server often lacks (they fail with exit 127). Prefer the wheel's copy when it
    actually runs, otherwise fall back to a system install (apt/PPA), so the same
    code works on a laptop and a bare VPS."""
    import shutil
    import subprocess

    candidates = [REPO / ".venv/bin" / name, shutil.which(name)]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            subprocess.run([str(candidate), "--version"],
                           check=True, capture_output=True)
            return str(candidate)
        except (OSError, subprocess.CalledProcessError):
            continue
    raise RuntimeError(
        f"no working '{name}' binary: the eclipse-sumo wheel's copy failed to run "
        f"(missing system libraries) and none is on PATH. Install SUMO system-wide, "
        f"e.g. 'sudo add-apt-repository ppa:sumo/stable && sudo apt install sumo'."
    )
