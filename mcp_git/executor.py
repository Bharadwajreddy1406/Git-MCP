import subprocess
from pathlib import Path
from mcp_git.config import load_config
import threading
import os


class GitExecutor:
    """
    Thread-safe singleton executor. Does not change global cwd; uses repo_root as cwd
    for git calls and resolves file paths relative to repo_root.
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # ensure __init__ runs only once
        if getattr(self, "_initialized", False):
            return
        self.config = load_config()
        self._initialized = True

    @staticmethod
    def instance() -> "GitExecutor":
        return GitExecutor()

    def git(self, args: list[str], allow_destructive=False) -> dict:
        repo_root = self.config.repo_root
        cwd = repo_root if repo_root is not None else None

        if not allow_destructive and self._is_destructive(args) and self._on_protected_branch(cwd=cwd):
            return {"ok": False, "error": "Protected branch. Destructive operation blocked."}

        return self._run_git(args, cwd=cwd)

    def read_file(self, path: str) -> dict:
        base = Path(self.config.repo_root) if self.config.repo_root else Path(".")
        p = Path(path)
        if not p.is_absolute():
            p = base / p
        return self._safe_read_file(p)

    def list_dir(self, path: str = ".") -> dict:
        base = Path(self.config.repo_root) if self.config.repo_root else Path(".")
        p = Path(path)
        if not p.is_absolute():
            p = base / p
        return self._safe_list_dir(p)

    def _run_git(self, args: list[str], cwd: str | None = None) -> dict:
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                check=True,
                cwd=cwd
            )
            return {"ok": True, "stdout": result.stdout.strip()}
        except subprocess.CalledProcessError as e:
            return {
                "ok": False,
                "error": e.stderr.strip() if e.stderr else "",
                "stdout": e.stdout.strip() if e.stdout else ""
            }

    def _on_protected_branch(self, cwd: str | None = None) -> bool:
        branch = self._run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd).get("stdout", "")
        return branch in self.config.protected_branches

    def _is_destructive(self, args: list[str]) -> bool:
        destructive_subcommands = {"reset", "rebase", "push", "checkout", "branch", "apply"}
        if not args:
            return False
        sub = args[0]
        if sub == "branch" and any(a in {"-D", "-d"} for a in args[1:]):
            return True
        if sub == "push" and any(a in {"--force", "-f"} for a in args[1:]):
            return True
        return sub in destructive_subcommands

    def _safe_read_file(self, p: Path) -> dict:
        if not p.exists():
            return {"ok": False, "error": f"File not found: {p}"}
        if p.is_dir():
            return {"ok": False, "error": f"Path is a directory: {p}"}
        try:
            return {"ok": True, "content": p.read_text()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _safe_list_dir(self, p: Path) -> dict:
        if not p.exists():
            return {"ok": False, "error": f"Directory not found: {p}"}
        files = [str(f) for f in p.rglob("*") if f.is_file()]
        return {"ok": True, "files": files}


# # legacy accessors
# def run_git(args: list[str], allow_destructive: bool = False) -> dict:
#     return GitExecutor.instance().git(args, allow_destructive=allow_destructive)

# def safe_read_file(path: str) -> dict:
#     return GitExecutor.instance().read_file(path)

# def safe_list_dir(path: str = ".") -> dict:
#     return GitExecutor.instance().list_dir(path)
