from mcp_git.tools.status import git_status
from mcp_git.tools.diff import git_diff
# from mcp_git.tools.commit import create_commit
from mcp_git.tools.switch_branch import switch_branch


print(git_status())
print(git_diff())
# print(create_commit(message="Test commit from mcp_git tools", add_all=True))

print("Test switch branch")
print(switch_branch("sample"))
print(switch_branch("main"))



