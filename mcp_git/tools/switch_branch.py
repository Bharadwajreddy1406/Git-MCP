from mcp_git.utils import branch_exists
from mcp_git.executors.git_executor import GitExecutor


def switch_branch(name: str) -> dict:
    if not branch_exists(name):
        return {"ok": False, "error": f"Branch '{name}' does not exist."}
    executor = GitExecutor.instance()
    return executor.git(["checkout", name], allow_destructive=True)
