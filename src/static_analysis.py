"""
Static analysis helpers.

Runs Pylint and Flake8 against a snippet of Python code and returns
their raw textual output so it can be shown to the user and/or fed
into the AI reviewer as extra context.
"""

import subprocess
import sys
import tempfile
import os


def _write_temp_file(code: str) -> str:
    """Write code to a temporary .py file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".py")
    with os.fdopen(fd, "w") as f:
        f.write(code)
    return path


def run_pylint(code: str) -> str:
    """Run pylint on the given code string and return its report."""
    path = _write_temp_file(code)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pylint", path, "--disable=C0114", "--score=y"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout or result.stderr
        # Replace the temp file's random name with something readable
        output = output.replace(path, "your_code.py")
        return output.strip() or "No issues found by Pylint."
    except FileNotFoundError:
        return "Pylint is not installed. Run: pip install pylint"
    except subprocess.TimeoutExpired:
        return "Pylint timed out while analyzing the code."
    finally:
        os.remove(path)


def run_flake8(code: str) -> str:
    """Run flake8 on the given code string and return its report."""
    path = _write_temp_file(code)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "flake8", path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = (result.stdout or result.stderr).replace(path, "your_code.py")
        return output.strip() or "No issues found by Flake8."
    except FileNotFoundError:
        return "Flake8 is not installed. Run: pip install flake8"
    except subprocess.TimeoutExpired:
        return "Flake8 timed out while analyzing the code."
    finally:
        os.remove(path)


def run_all(code: str) -> dict:
    """Run all static analyzers and return a dict of {tool_name: report}."""
    return {
        "pylint": run_pylint(code),
        "flake8": run_flake8(code),
    }
