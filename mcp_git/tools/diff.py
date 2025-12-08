from mcp_git.executors.git_executor import GitExecutor
from mcp_git.enums import RepoArea

def git_diff(target: str = RepoArea.WORKING.value, commit_a: str = None, commit_b: str = None) -> dict:
    """Return a unified diff between working tree, staged changes, or two commits."""
    executor = GitExecutor.instance()
    args = ["diff"]
    meta = {"type": target}

    if commit_a and commit_b:
        args.extend([commit_a, commit_b])
        meta["type"] = "commit"
        meta["commits"] = [commit_a, commit_b]
    elif target == RepoArea.STAGED.value:
        args.append("--staged")
    # No special args for RepoArea.WORKING, it's the default

    result = executor.git(args)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to compute diff: {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": meta,
    }

