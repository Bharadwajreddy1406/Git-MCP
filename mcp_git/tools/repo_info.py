from mcp_git.executor import GitExecutor


def repo_info() -> dict:
    """Return basic repository metadata using GitExecutor."""
    executor = GitExecutor.instance()
    branch = executor.git(["rev-parse", "--abbrev-ref", "HEAD"]).get("stdout")
    remotes = executor.git(["remote", "-v"]).get("stdout")
    last_commit = executor.git(["log", "-1", "--pretty=format:%H%n%s"]).get("stdout")
    return {"ok": True, "branch": branch, "remotes": remotes, "last_commit": last_commit}
