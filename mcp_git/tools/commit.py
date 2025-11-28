from mcp_git.executor import GitExecutor


def create_commit(message: str, add_all: bool = False) -> dict:
    executor = GitExecutor.instance()
    if add_all:
        stage = executor.git(["add", "-A"], allow_destructive=True)
        if not stage.get("ok"):
            return stage

    commit = executor.git(["commit", "-m", message], allow_destructive=True)
    if not commit.get("ok"):
        return commit

    last_hash = executor.git(["rev-parse", "HEAD"])
    commit["commit_hash"] = last_hash.get("stdout")
    return commit
