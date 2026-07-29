"""Backward-compatible wrapper: build all sample ZIPs. """

from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).with_name("build_sample_skills.py")), run_name="__main__")
