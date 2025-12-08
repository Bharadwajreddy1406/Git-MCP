from mcp_git.executors.git_executor import GitExecutor
from mcp_git.utils import branch_exists

def create_branch(name: str, checkout: bool = True) -> dict:
    """Create a new branch and optionally check it out."""
    executor = GitExecutor.instance()

    # 1. Pre-validation: Check if branch already exists
    if branch_exists(name):
        return {
            "ok": False,
            "stdout": "",
            "stderr": f"Branch '{name}' already exists.",
            "error": f"Branch '{name}' already exists.",
            "meta": None,
        }

    # 2. Create the branch
    args = ["branch", name]
    if checkout:
        args = ["checkout", "-b", name]

    result = executor.git(args, allow_destructive=True)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to create branch '{name}': {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"branch": name, "checked_out": checkout},
    }

