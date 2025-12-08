from mcp_git.executors.git_executor import GitExecutor

def pop_stash(stash_name : str = "stash@{0}") -> dict:
    """Pop the most recent stash or a specified stash."""
    executor = GitExecutor.instance()
    result = executor.git(["stash", "pop", stash_name], allow_destructive=True)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to pop stash '{stash_name}': {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"stash": stash_name},
    }