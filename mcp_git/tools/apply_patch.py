from mcp_git.executors.git_executor import GitExecutor

def apply_patch(patch: str) -> dict:
    """Apply a unified diff patch safely."""
    executor = GitExecutor.instance()
    
    # The `git apply` command can be destructive, so we check the branch
    result = executor.git(["apply", "--reject", "--whitespace=fix"], allow_destructive=True)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to apply patch: {result['error']}",
            "meta": None,
        }

    # Check for .rej files which indicate a failed patch application
    status_result = executor.git(["status", "--porcelain"])
    if ".rej" in status_result.get("stdout", ""):
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": "Patch application resulted in .rej files. Please resolve conflicts manually.",
            "error": "Patch application failed with conflicts.",
            "meta": {"conflicts": True},
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"conflicts": False},
    }

