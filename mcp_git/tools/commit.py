from mcp_git.executors.git_executor import GitExecutor

def create_commit(message: str, add_all: bool = False) -> dict:
    """Stage changes and create a commit with the given message."""
    executor = GitExecutor.instance()

    if add_all:
        stage_result = executor.git(["add", "-A"], allow_destructive=True)
        if not stage_result["ok"]:
            return {
                "ok": False,
                "stdout": stage_result["stdout"],
                "stderr": stage_result["stderr"],
                "error": f"Failed to stage all changes: {stage_result['error']}",
                "meta": None,
            }

    commit_result = executor.git(["commit", "-m", message], allow_destructive=True)
    if not commit_result["ok"]:
        return {
            "ok": False,
            "stdout": commit_result["stdout"],
            "stderr": commit_result["stderr"],
            "error": f"Failed to create commit: {commit_result['error']}",
            "meta": None,
        }

    # After a successful commit, get the new commit hash
    hash_result = executor.git(["rev-parse", "HEAD"])
    if not hash_result["ok"]:
        return {
            "ok": False,
            "stdout": hash_result["stdout"],
            "stderr": hash_result["stderr"],
            "error": "Commit was created, but failed to retrieve the new commit hash.",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": commit_result["stdout"],
        "stderr": commit_result["stderr"],
        "error": None,
        "meta": {"commit_hash": hash_result["stdout"]},
    }

