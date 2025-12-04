from mcp_git.executors.git_executor import GitExecutor


def list_files(path: str = ".") -> dict:
    executor = GitExecutor.instance()
    return executor.list_dir(path)
