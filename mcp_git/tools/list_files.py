from mcp_git.executors.fs_executor import FsExecutor

def list_files(path: str = ".") -> dict:
    """Recursively list all files under the specified directory."""
    executor = FsExecutor.instance()
    result = executor.list_dir(path)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": "",
            "stderr": result["error"],
            "error": result["error"],
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": "\n".join(result["files"]),
        "stderr": "",
        "error": None,
        "meta": {"count": len(result["files"]), "path": path},
    }

