from mcp_git.executors.fs_executor import FsExecutor
import os

def read_file(path: str) -> dict:
    """Read the content of a file safely."""
    executor = FsExecutor.instance()
    result = executor.read_file(path)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": "",
            "stderr": result["error"],
            "error": result["error"],
            "meta": None,
        }

    # Get file size for metadata
    p = executor._common_path_preprocessing(path)
    file_size = os.path.getsize(p)

    return {
        "ok": True,
        "stdout": result["content"],
        "stderr": "",
        "error": None,
        "meta": {"path": path, "size": file_size},
    }

