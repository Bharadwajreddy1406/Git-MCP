from mcp.server.fastmcp import FastMCP
from mcp_git.tools.repo_info import repo_info
from mcp_git.tools.status import git_status
from mcp_git.tools.list_files import list_files
from mcp_git.tools.read_file import read_file
from mcp_git.tools.diff import git_diff
from mcp_git.tools.apply_patch import apply_patch
from mcp_git.tools.create_branch import create_branch
from mcp_git.tools.commit import create_commit

mcp = FastMCP(
    name="git-mcp-server",
    # description="Python-based MCP server exposing Git operations"
)

# ---------------------------
# REGISTER ALL YOUR TOOLS HERE
# ---------------------------

@mcp.tool()
def git_repo_info() -> dict:
    return repo_info()

@mcp.tool()
def git_status_tool() -> dict:
    return git_status()

@mcp.tool()
def git_list_files(path: str = ".") -> dict:
    return list_files(path)

@mcp.tool()
def git_read_file(path: str) -> dict:
    return read_file(path)

@mcp.tool()
def git_diff_tool(
    target: str = "working",
    commit_a: str = None,
    commit_b: str = None
) -> dict:
    return git_diff(target, commit_a, commit_b)

@mcp.tool()
def git_apply_patch(patch: str) -> dict:
    return apply_patch(patch)

@mcp.tool()
def git_create_branch(name: str, checkout: bool = True) -> dict:
    return create_branch(name, checkout)

@mcp.tool()
def git_commit(message: str, add_all: bool = False) -> dict:
    return create_commit(message, add_all)


# Run the MCP Server
if __name__ == "__main__":
    mcp.run()
