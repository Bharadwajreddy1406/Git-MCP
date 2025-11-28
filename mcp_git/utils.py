from mcp_git.executor import GitExecutor


def branch_exists(name: str) -> bool:
    executor = GitExecutor.instance()
    result = executor.git(["branch", "--list", name])
    return bool(result.get("stdout", "").strip())
