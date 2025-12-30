# ServiceNow MCP Server (Pinned Tooling Repo)

This directory is reserved for the ServiceNow MCP server repository. The main repo
remains the deliverable; this tooling repo is the bridge that touches ServiceNow.

## How to pin the MCP server
Use a git submodule or a vendored repo pinned to a specific commit:

```bash
git submodule add <MCP_SERVER_REPO_URL> tools/servicenow-mcp
git submodule update --init --recursive
```

Record the pinned commit SHA here once added.

## Start command
Document the exact startup command for your MCP server here (local + CI).

Example (replace with real command):
```bash
cd tools/servicenow-mcp
<start-command>
```
