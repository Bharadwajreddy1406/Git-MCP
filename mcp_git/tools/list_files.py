from mcp_git.executor import GitExecutor


def list_files(path: str = ".") -> dict:
    executor = GitExecutor.instance()
    return executor.list_dir(path)
