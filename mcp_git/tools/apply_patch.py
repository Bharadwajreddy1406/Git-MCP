import subprocess


def apply_patch(patch: str) -> dict:
    """
    Apply a unified diff patch safely.
    """

    try:
        proc = subprocess.run(
            ["git", "apply", "--reject", "--whitespace=fix"],
            input=patch,
            text=True,
            capture_output=True,
            check=True
        )
        return {"ok": True}
    except subprocess.CalledProcessError as e:
        return {
            "ok": False,
            "error": e.stderr.strip(),
            "stdout": e.stdout.strip(),
        }
