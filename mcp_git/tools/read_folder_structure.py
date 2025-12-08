from mcp_git.executors.fs_executor import FsExecutor

def read_folder_structure(base_path: str = None, skip_gitignore: bool = True) -> dict:
    """
    Returns a tree-like view of the repository structure.
    """
    executor = FsExecutor.instance()
    
    path_to_scan = base_path if base_path else "."
    
    result = executor.tree_view(path_to_scan, use_gitignore=skip_gitignore)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": "",
            "stderr": result["error"],
            "error": f"Failed to read folder structure: {result['error']}",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["tree"],
        "stderr": "",
        "error": None,
        "meta": {"path": path_to_scan, "gitignore_skipped": skip_gitignore},
    }