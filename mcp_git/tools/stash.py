from mcp_git.executors.git_executor import GitExecutor


def stash_changes(message: str = "WIP", stash_unstaged: bool = False) -> dict:
    """Stash current changes with an optional message."""
    executor = GitExecutor.instance()
    if stash_unstaged:
        result = executor.git(
            ["stash", "push", "-u", "-m", message], allow_destructive=True
        )
    else:
        result = executor.git(["stash", "push", "-m", message], allow_destructive=True)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to stash changes: {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"message": message},
    }
