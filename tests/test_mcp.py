from mcp_git.tools.status import git_status
from mcp_git.tools.diff import git_diff
# from mcp_git.tools.commit import create_commit
from mcp_git.tools.switch_branch import switch_branch
from mcp_git.utils import branch_exists
from mcp_git.tools.list_files import list_files
from mcp_git.tools.read_folder_structure import read_folder_structure
from mcp_git.tools.stash import stash_changes
from mcp_git.tools.list_stashes import list_stashes
from mcp_git.tools.pop_stash import pop_stash

from mcp_git.config import load_config
from mcp_git.executors.fs_executor import FsExecutor
import os

print("#"*80)
print("Tests for MCP Read Only tools")
print("#"*80)

def test_git_status():
    result = git_status()
    assert result["ok"], f"git_status failed: {result['error']}"
    print(" git status result:", result)
    print("git_status passed.")
    
    
def test_git_diff():
    result = git_diff()
    assert result["ok"], f"git_diff failed: {result['error']}"
    print(" git diff result:", result)
    print("git_diff passed.")
    
def test_switch_branch_tool():
    test_branch = "demo"
    status = git_status()
    
    if status["ok"] and status["stdout"] != "":
        print("Repository has uncommitted changes. Please commit or stash them before running switch_branch_tool_test.")
        return
    # Ensure the test branch exists
    if not branch_exists(test_branch):
        print(f"Creating test branch '{test_branch}' for switch_branch test.")
        create_result = switch_branch("main")  # Switch to main first
        assert create_result["ok"], f"Failed to switch to main: {create_result['error']}"
        create_result = switch_branch(test_branch)
        assert create_result["ok"], f"Failed to create test branch: {create_result['error']}"
    
    result = switch_branch(test_branch)
    assert result["ok"], f"switch_branch failed: {result['error']}"
    print(" switch branch result:", result)
    print("Switching back to main branch.")
    switch_branch("main")  
    print("switch_branch passed.")
    
def listing_files_tool_test():
    config = load_config()
    result = list_files(config.repo_root)
    assert result["ok"], f"list_files failed: {result['error']}"
    print(" list files result:", result)
    print("list_files passed.")

def read_folder_structure_tool_test():
    config = load_config()
    result = read_folder_structure(config.repo_root)
    assert result["ok"], f"read_dir failed: {result['error']}"
    print(" read dir result:", result)
    print("read_dir passed.")
    
def list_stashes_tool_test():
    
    result = list_stashes()
    assert result["ok"], f"list_stashes failed: {result['error']}"
    print(" list stashes result:", result)
    print("list_stashes passed.")
    
    
def stash_tool_test():
    
    status = git_status()
    if status["ok"] and status["stdout"] != "":
        
        result = stash_changes("Test stash from MCP", stash_unstaged=True)
        assert result["ok"], f"stash_changes failed: {result['error']}"
        print(" stash changes result:", result)
    else:
        config = load_config()
        os.chdir(config.repo_path)
        os.makefile("temp_test_file.txt", mode=0o644, exist_ok=True)
        result = stash_changes("Test stash from MCP", stash_unstaged=True)
        result = stash_changes("Test stash from MCP", stash_unstaged=True)
        assert result["ok"], f"stash_changes failed: {result['error']}"
        print(" stash changes result:", result)
        print("stash_changes passed.")

def pop_stash_tool_test():
    
    stashes = list_stashes()
    if stashes["ok"] and stashes["meta"]["count"] > 0:
        result = pop_stash(0)
        assert result["ok"], f"pop_stash failed: {result['error']}"
        print(" pop stash result:", result)
        print("pop_stash passed.")
    else:
        print("No stashes to pop. Skipping pop_stash test.")
        
        
def run_all_RO_tests():
    test_git_status()
    test_git_diff()
    test_switch_branch_tool()
    listing_files_tool_test()
    read_folder_structure_tool_test()
    list_stashes_tool_test()
    stash_tool_test()
    pop_stash_tool_test()
    
    

run_all_RO_tests()

