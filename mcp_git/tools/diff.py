from mcp_git.executors.git_executor import GitExecutor
from mcp_git.enums import RepoArea


def git_diff(target: str = RepoArea.WORKING.value, commit_a: str = None, commit_b: str = None) -> dict:
    executor = GitExecutor.instance()
    if commit_a and commit_b:
        return executor.git(["diff", commit_a, commit_b])
    if target == RepoArea.STAGED.value:
        return executor.git(["diff", "--staged"])
    return executor.git(["diff"])
