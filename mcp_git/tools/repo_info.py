from mcp_git.executors.git_executor import GitExecutor

def repo_info() -> dict:
    """Get metadata about the current Git repository."""
    executor = GitExecutor.instance()

    # 1. Get current branch
    branch_result = executor.git(["rev-parse", "--abbrev-ref", "HEAD"])
    if not branch_result["ok"]:
        return {
            "ok": False,
            "stdout": "",
            "stderr": "Could not determine current branch.",
            "error": "Failed to get repository info: could not determine current branch.",
            "meta": None,
        }
    branch = branch_result["stdout"]

    # 2. Get remotes
    remotes_result = executor.git(["remote", "-v"])
    remotes = remotes_result["stdout"] if remotes_result["ok"] else "Could not fetch remotes."

    # 3. Get last commit
    commit_result = executor.git(["log", "-1", "--pretty=format:%H (%s)"])
    last_commit = commit_result["stdout"] if commit_result["ok"] else "Could not fetch last commit."

    return {
        "ok": True,
        "stdout": f"Branch: {branch}\nRemotes:\n{remotes}\nLast Commit: {last_commit}",
        "stderr": "",
        "error": None,
        "meta": {
            "branch": branch,
            "remotes": remotes.splitlines(),
            "last_commit": last_commit,
        },
    }

