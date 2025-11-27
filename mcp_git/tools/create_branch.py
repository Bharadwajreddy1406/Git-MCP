from mcp_git.executor import run_git


def create_branch(name: str, checkout: bool = True) -> dict:
    create = run_git(["branch", name])
    if not create["ok"]:
        return create

    if checkout:
        return run_git(["checkout", name])

    return {"ok": True, "message": f"Branch '{name}' created"}
