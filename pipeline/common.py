"""Shared pipeline constants and helpers."""

import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def pdf_text(path):
    return subprocess.run(
        ["pdftotext", "-layout", str(path), "-"],
        capture_output=True, text=True, check=True).stdout
