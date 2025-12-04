from mcp_git.executors.git_executor import GitExecutor


def read_file(path: str) -> dict:
    executor = GitExecutor.instance()
    return executor.read_file(path)
