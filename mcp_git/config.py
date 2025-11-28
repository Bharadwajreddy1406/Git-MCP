from pathlib import Path
import os

class GitMCPConfig:
    def __init__(self):
        self.repo_root = Path(os.getenv("GIT_MCP_REPO_ROOT", ".")).resolve()
        self.default_remote = os.getenv("GIT_MCP_REMOTE", "origin")
        self.protected_branches = [
            b.strip()
            for b in os.getenv("GIT_MCP_PROTECTED_BRANCHES", "main,master").split(",")
            if b.strip()
        ]
        self.dry_run = os.getenv("GIT_MCP_DRY_RUN", "false").lower() == "true"
        self.max_patch_size = int(os.getenv("GIT_MCP_MAX_PATCH_SIZE", 50000))
        self.max_changed_files = int(os.getenv("GIT_MCP_MAX_CHANGED_FILES", 50))
        self.enable_logging = os.getenv("GIT_MCP_LOGGING", "true").lower() == "true"
        self.log_path = Path(os.getenv("GIT_MCP_LOG_PATH", "./mcp_git.log"))


_config_instance: GitMCPConfig | None = None


def load_config() -> GitMCPConfig:
    global _config_instance
    if _config_instance is None:
        _config_instance = GitMCPConfig()
    return _config_instance
