from mcp_git.executor import GitExecutor
from mcp_git.tools.switch_branch import switch_branch


def create_branch(name: str, checkout: bool = True) -> dict:
    executor = GitExecutor.instance()
    create = executor.git(["branch", name], allow_destructive=True)
    if not create.get("ok"):
        return create
    if checkout:
        return switch_branch(name)
    return {"ok": True, "message": f"Branch '{name}' created"}
