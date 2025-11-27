from mcp_git.executor import run_git


def repo_info() -> dict:
    """
    Returns:
    - repo path
    - current branch
    - remotes
    - latest commit hash & message
    """

    # Current branch
    branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])

    # Remotes
    remotes = run_git(["remote", "-v"])

    # Latest commit
    last_commit = run_git(["log", "-1", "--pretty=format:%H%n%s"])

    return {
        "ok": True,
        "branch": branch.get("stdout"),
        "remotes": remotes.get("stdout"),
        "last_commit": last_commit.get("stdout"),
    }
