from mcp_git.executor import run_git


def create_commit(message: str, add_all: bool = False) -> dict:
    if add_all:
        stage = run_git(["add", "-A"])
        if not stage["ok"]:
            return stage

    commit = run_git(["commit", "-m", message])
    if not commit["ok"]:
        return commit

    # return commit hash
    last_hash = run_git(["rev-parse", "HEAD"])
    commit["commit_hash"] = last_hash.get("stdout")

    return commit
