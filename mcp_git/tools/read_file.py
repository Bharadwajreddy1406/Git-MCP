from mcp_git.executor import safe_read_file


def read_file(path: str) -> dict:
    return safe_read_file(path)
