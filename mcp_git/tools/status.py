from mcp_git.executor import GitExecutor


def git_status() -> dict:
    executor = GitExecutor.instance()
    result = executor.git(["status", "--porcelain"])
    if not result.get("ok"):
        return result
    stdout = result.get("stdout", "")
    changes = []
    for line in stdout.splitlines():
        if not line.strip():
            continue
        status = line[:2].strip()
        path = line[3:].strip()
        changes.append({"status": status, "path": path})
    return {"ok": True, "changes": changes}
