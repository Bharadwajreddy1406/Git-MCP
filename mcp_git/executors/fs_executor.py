from __future__ import annotations
from mcp_git.config import load_config
import threading
import os
import subprocess as terminal
from pathlib import Path

class FsExecutor:
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        with self._lock:
            if self._initialized:
                return
            self.config = load_config()
            self._initialized = True
        
    @staticmethod
    def instance() -> FsExecutor:
        return FsExecutor()
    
    def _common_path_preprocessing(self, path: str) -> Path:
        base = Path(self.config.repo_root) if self.config.repo_root else Path(".")
        p = Path(path)
        if not p.is_absolute():
            p = base / p
        return p
    
    def know_os(self) -> str:
        return os.name

    def list_dir(self, path: str = ".", use_gitignore: bool = True) -> dict:
        p = self._common_path_preprocessing(path)
        try:
            if not p.exists() or not p.is_dir():
                return {"ok": False, "error": f"Path '{p}' does not exist or is not a directory."}

            files = []
            
            gitignore_patterns = []
            if use_gitignore:
                gitignore_path = Path(self.config.repo_root) / ".gitignore" if self.config.repo_root else Path(".gitignore")
                if gitignore_path.exists():
                    with gitignore_path.open("r", encoding="utf-8") as f:
                        gitignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]

            for root, _, filenames in os.walk(p):
                for filename in filenames:
                    file_path = Path(root) / filename
                    
                    # Gitignore check
                    if use_gitignore and self._is_ignored(file_path, gitignore_patterns):
                        continue
                        
                    files.append(str(file_path.relative_to(p)))

            return {"ok": True, "files": files}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def _is_ignored(self, path: Path, patterns: list[str]) -> bool:
        import fnmatch
        for pattern in patterns:
            if fnmatch.fnmatch(path.name, pattern) or any(fnmatch.fnmatch(part, pattern) for part in path.parts):
                return True
        return False
        
    def read_file(self, path: str) -> dict:
        p = self._common_path_preprocessing(path)
        try:
            if not p.exists() or not p.is_file():
                return {"ok": False, "error": f"File '{p}' does not exist or is not a file."}
            with p.open("r", encoding="utf-8") as f:
                content = f.read()
            return {"ok": True, "content": content}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def make_directory(self, path: str) -> dict:
        p = self._common_path_preprocessing(path)

        try:
            p.mkdir(parents=True, exist_ok=True)
            return {"ok": True, "message": f"Directory '{p}' created successfully."}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        
    def change_directory(self,path : str) -> dict:
        p = self._common_path_preprocessing(path)
        try:
            if not p.exists() or not p.is_dir():
                return {"ok": False, "error": f"Path '{p}' does not exist or is not a directory."}
            os.chdir(p)
            return {"ok": True, "message": f"Changed current directory to '{p}'."}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        
    def tree_view(self, path : str = ".", use_gitignore = False) -> dict:
        p = self._common_path_preprocessing(path)
        try:
            if not p.exists() or not p.is_dir():
                return {"ok": False, "error": f"Path '{p}' does not exist or is not a directory."}
            if use_gitignore:
                gitignore_path = p / ".gitignore"
                if gitignore_path.exists():
                    with gitignore_path.open("r", encoding="utf-8") as f:
                        gitignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith("#")]
                    gitignore_args = []
                    for pattern in gitignore_patterns:
                        gitignore_args.extend(["-I", pattern])
                    result = terminal.run(["tree", str(p), *gitignore_args], capture_output=True, text=True)
                else:
                    result = terminal.run(["tree", str(p)], capture_output=True, text=True)
            else:
                result = terminal.run(["tree", str(p)], capture_output=True, text=True)
                
            if result.returncode != 0:
                return {"ok": False, "error": result.stderr}
            return {"ok": True, "tree": result.stdout}
        except Exception as e:
            return {"ok": False, "error": str(e)}
