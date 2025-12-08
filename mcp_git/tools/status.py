from mcp_git.executors.git_executor import GitExecutor


def git_status() -> dict:
    """Return machine-readable Git status information."""
    executor = GitExecutor.instance()
    result = executor.git(["status", "--porcelain"])

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to get git status: {result['error']}",
            "meta": None,
        }

    stdout = result.get("stdout", "")
    changes = []
    if stdout:
        for line in stdout.splitlines():
            if len(line) > 2:
                status, file = line[:2], line[3:]
                changes.append({"status": status.strip(), "file": file.strip()})

    return {
        "ok": True,
        "stdout": stdout,
        "stderr": result["stderr"],
        "error": None,
        "meta": {"changes": changes, "count": len(changes)},
    }
