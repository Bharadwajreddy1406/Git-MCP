from mcp_git.utils import branch_exists
from mcp_git.executors.git_executor import GitExecutor

def switch_branch(name: str) -> dict:
    """Switch to the specified branch."""
    executor = GitExecutor.instance()

    # 1. Pre-validation: Check if branch exists
    if not branch_exists(name):
        return {
            "ok": False,
            "stdout": "",
            "stderr": f"Branch '{name}' does not exist.",
            "error": f"Branch '{name}' does not exist.",
            "meta": None,
        }

    # 2. Switch branch
    result = executor.git(["checkout", name], allow_destructive=True)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to switch to branch '{name}': {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"branch": name},
    }

