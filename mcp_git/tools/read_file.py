from mcp_git.executor import GitExecutor


def read_file(path: str) -> dict:
    executor = GitExecutor.instance()
    return executor.read_file(path)
