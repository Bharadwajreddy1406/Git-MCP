from mcp.server.fastmcp import FastMCP
from mcp_git.tools.repo_info import repo_info
from mcp_git.tools.status import git_status
from mcp_git.tools.list_files import list_files
from mcp_git.tools.read_file import read_file
from mcp_git.tools.switch_branch import switch_branch
from mcp_git.tools.diff import git_diff
from mcp_git.tools.apply_patch import apply_patch
from mcp_git.tools.create_branch import create_branch
from mcp_git.tools.commit import create_commit
from mcp_git.tools.read_folder_structure import read_folder_structure
from mcp_git.enums import MCPVersion, RepoArea

import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP(
    name=f"git-mcp-server version : {MCPVersion.V1_0.value} ",
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
    target: str = RepoArea.WORKING.value, commit_a: str = None, commit_b: str = None
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

@mcp.tool()
def git_switch_branch(name: str) -> dict:
    return switch_branch(name)

@mcp.tool()
def folder_structure_reader(base_path: str = None, skip_gitignore: bool = True) -> dict:
    return read_folder_structure(base_path, skip_gitignore)

# Run the MCP Server
if __name__ == "__main__":
    mcp.run()
