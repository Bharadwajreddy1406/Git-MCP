import subprocess
import json
from pathlib import Path


def run_git(args: list[str]) -> dict:
    """
    Run a git command safely and return structured output.
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return {"ok": True, "stdout": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {
            "ok": False,
            "error": e.stderr.strip(),
            "stdout": e.stdout.strip() if e.stdout else ""
        }


def safe_read_file(path: str) -> dict:
    """
    Safely read a file from disk.
    """
    p = Path(path)

    if not p.exists():
        return {"ok": False, "error": f"File not found: {path}"}

    if p.is_dir():
        return {"ok": False, "error": f"Path is a directory: {path}"}

    try:
        return {"ok": True, "content": p.read_text()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def safe_list_dir(path: str = ".") -> dict:
    """
    Recursively list all files.
    """
    p = Path(path)

    if not p.exists():
        return {"ok": False, "error": f"Directory not found: {path}"}

    files = []
    for file in p.rglob("*"):
        if file.is_file():
            files.append(str(file))

    return {"ok": True, "files": files}
