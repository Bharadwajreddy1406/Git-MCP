from mcp_git.executor import run_git


def git_diff(target: str = "working", commit_a: str = None, commit_b: str = None) -> dict:
    """
    target="working" → working tree diff
    target="staged" → staged diff
    commit_a + commit_b → commit-to-commit diff
    """

    if commit_a and commit_b:
        return run_git(["diff", commit_a, commit_b])

    if target == "staged":
        return run_git(["diff", "--staged"])

    return run_git(["diff"])
