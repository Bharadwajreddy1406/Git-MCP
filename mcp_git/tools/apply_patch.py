import subprocess
from mcp_git.executor import GitExecutor


def apply_patch(patch: str) -> dict:
    """Apply a unified diff patch safely using GitExecutor context."""
    executor = GitExecutor.instance()

    # Honor protected branch policy (treat apply as destructive)
    if executor._on_protected_branch() and executor._is_destructive(["apply"]):  # type: ignore
        return {"ok": False, "error": "Protected branch. Patch application blocked."}

    try:
        result = subprocess.run(
            ["git", "apply", "--reject", "--whitespace=fix"],
            input=patch,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            return {
                "ok": False,
                "error": result.stderr.strip(),
                "stdout": result.stdout.strip(),
            }
        return {"ok": True}
    except Exception as e:
        return {"ok": False, "error": str(e)}
