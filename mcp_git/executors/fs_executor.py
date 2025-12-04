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
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._initialized = True
        return cls._instance
    
    def __init__(self):
        # ensure __init__ runs only once
        if getattr(self, "_initialized", False):
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

    def list_dir(self, path: str = ".") -> dict:
        p = self._common_path_preprocessing(path)
        try:
            if not p.exists() or not p.is_dir():
                return {"ok": False, "error": f"Path '{p}' does not exist or is not a directory."}
            items = [item.name for item in p.iterdir()]
            return {"ok": True, "items": items}
        except Exception as e:
            return {"ok": False, "error": str(e)}
        
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
    
    
    