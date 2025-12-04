from subprocess import CalledProcessError, run
from pathlib import Path
from mcp_git.config import load_config

cfg = load_config()

def read_folder_structure(base_path: str = cfg.repo_root, skip_gitignore=True) -> dict:
    """
    Reads the folder structure starting from base_path and returns it as a nested dictionary.
    Directories are represented as dictionaries and files as None.
    Uses `git check-ignore` to skip files/folders ignored by git when skip_gitignore is True.
    """
    base = Path(base_path) if base_path else Path(".")
    if not base.exists() or not base.is_dir():
        return {"ok": False, "error": f"Path '{base}' does not exist or is not a directory."}

    def _is_ignored_by_git(path: Path) -> bool:
        if not skip_gitignore:
            return False
        try:
            
            if path.parts[0] == '.git':
                return True
            # run git check-ignore in the repo root so .gitignore rules are resolved properly
            cp = run(["git", "check-ignore", "-q", str(path)], cwd=base, capture_output=True)
            return cp.returncode == 0
        except FileNotFoundError:
            # git not available -> treat as not ignored
            return False
        except Exception:
            # any other git error -> treat as not ignored
            return False

    def _read_dir(path: Path) -> dict:
        structure = {}
        for item in path.iterdir():
            if _is_ignored_by_git(item):
                continue
            if item.is_dir():
                structure[item.name] = _read_dir(item)
            else:
                structure[item.name] = None
        return structure

    folder_structure = _read_dir(base)
    return {"ok": True, "structure": folder_structure}