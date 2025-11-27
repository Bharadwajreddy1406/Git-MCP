from mcp_git.executor import run_git


def git_status() -> dict:
    """
    Machine-readable git status
    """
    result = run_git(["status", "--porcelain"])

    if not result["ok"]:
        return result

    changes = []
    for line in result["stdout"].splitlines():
        if not line.strip():
            continue

        status = line[:2].strip()
        path = line[3:].strip()
        changes.append({"status": status, "path": path})

    return {"ok": True, "changes": changes}
