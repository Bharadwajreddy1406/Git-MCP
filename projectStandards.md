# 📘 **MCP Git – Standardized Return Contract & Error Handling Specification**

### **Version 1.0 — Authoritative Guideline for All Tools**

This is the **single source of truth** for return structures, error handling, and consistency across all git-related MCP tools.
Follow this document for every new tool, refactor, or bugfix.
---
# 🔥 **1. Core Principle**

Every MCP git tool **must** return a **uniform response structure** so that:
* Clients parsing MCP responses know what to expect
* Higher-level tools can compose behavior safely
* Errors never propagate as "pretend successes"
* Testing becomes deterministic
* Tooling behaves like a real API, not a script dump

---
# 📦 **2. Standard Response Format**
Every tool MUST return an object with the following fields:
```json
{
  "ok": true/false,
  "stdout": "<string>",
  "stderr": "<string>",
  "error": "<string | null>",
  "meta": { ... optional metadata ... }
}
```

### **Field definitions**

| Field    | Description                                                    |
| -------- | -------------------------------------------------------------- |
| `ok`     | Boolean success flag. **Must reflect actual Git outcome.**     |
| `stdout` | stdout content from underlying git calls. Always included.     |
| `stderr` | stderr output from git. Must be included even if empty.        |
| `error`  | Developer-friendly error message. `null` if success.           |
| `meta`   | Optional structured output (like parsed lists, hashes, stats). |

---
# 🔧 **3. Rules For Tool Authors**

### **Rule 1: Never overwrite Git failure with success.**
If `run_git()` returns `ok: False` → your tool must return failure.
### **Rule 2: Your tool may add validation, but never hide Git’s own errors.**
### **Rule 3: Tool-specific errors must populate the `error` field, not raise exceptions.**
### **Rule 4: All tools must wrap non-git logic in the same contract.**

---
# 🧱 **4. Standardized `run_git()` Contract**
Your `run_git` must be the *foundation* and return:
```python
{
  "ok": True/False,
  "stdout": <string>,
  "stderr": <string>,
  "error": <string or None>,
}
```
This becomes the canonical wrapper.

---
# 🧭 **5. Recommended Tool Skeleton (USE THIS TEMPLATE)**

All tools should follow this structure:

```python
from mcp_git.executor import run_git

def TOOL_NAME(args...) -> dict:
    # 1. optional pre-validation
    # 2. call git
    result = run_git([...])
    
    # 3. respect git result
    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": result["error"] or "Git command failed.",
            "meta": None,
        }

    # 4. attach meta output (optional)
    meta = {
        # structured additional data
    }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": meta,
    }
```

This eliminates:

* fake success conditions
* inconsistent return shapes
* missing stderr
* missing metadata
* vague behavior

---

# 📌 **6. Examples of Proper Tools**

### **6.1 switch_branch**

```python
def switch_branch(name: str) -> dict:
    result = run_git(["checkout", name])

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": f"Failed to switch branch '{name}'",
            "meta": None
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": { "branch": name }
    }
```

---

### **6.2 git_diff**

```python
def git_diff(target="working", commit_a=None, commit_b=None):
    args = ["diff"]

    if commit_a and commit_b:
        args += [commit_a, commit_b]
    elif target == "staged":
        args += ["--staged"]

    result = run_git(args)

    if not result["ok"]:
        return {
            "ok": False,
            "stdout": result["stdout"],
            "stderr": result["stderr"],
            "error": "Failed to compute diff",
            "meta": None,
        }

    return {
        "ok": True,
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "error": None,
        "meta": {"type": target},
    }
```

---

# 🧩 **7. Meta Field Guidelines**

The `meta` field must contain predictable, structured data — for example:

* lists of branches
* diff summary
* commit metadata
* changed file counts
* line stats

This allows future clients to build UIs or automations on top.

---

# 🚨 **8. Error Messages**

Error messages must be:

* human-friendly
* not Git's raw wall of text
* one clear sentence explaining the failure

Example:

❌ “fatal: ambiguous argument”
✔️ “Cannot compute diff: invalid commit range provided.”

---
