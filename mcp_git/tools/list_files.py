from mcp_git.executor import safe_list_dir


def list_files(path: str = ".") -> dict:
    return safe_list_dir(path)
