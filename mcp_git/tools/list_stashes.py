from mcp_git.executors.git_executor import GitExecutor


def list_stashes() -> dict:
    """List all git stashes in the repository."""
    executor = GitExecutor.instance()
    result = executor.git(["stash", "list"])

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to list stashes: {result['error']}",
            "meta": None,
        }

    stashes = []
    stdout = result.get("stdout", "")
    if stdout:
        for line in stdout.splitlines():
            parts = line.split(":", 2)
            if len(parts) == 3:
                stash_id, branch_info, message = parts
                stashes.append(
                    {
                        "id": stash_id.strip(),
                        "branch": branch_info.strip(),
                        "message": message.strip(),
                    }
                )

    return {
        "ok": True,
        "stdout": stdout,
        "stderr": result["stderr"],
        "error": None,
        "meta": {"stashes": stashes, "count": len(stashes)},
    }
