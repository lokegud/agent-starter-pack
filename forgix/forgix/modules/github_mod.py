"""
Forgix GitHub module — GitHub REST API integration.
Permissions: read_github, write_github
"""
from __future__ import annotations

from typing import Callable

import httpx

from forgix.modules.base import BaseModule, ModuleManifest, tool_schema


class GithubModule(BaseModule):
    manifest = ModuleManifest(
        name="github",
        version="0.1.0",
        description="GitHub REST API — search repos, manage issues, read code",
        required_permissions=["read_github", "write_github", "network"],
    )

    def __init__(self):
        token = self._get_secret("module_github_github_token") or ""
        self._headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"} if token else {}
        self._base = "https://api.github.com"

    def get_tools(self) -> dict[str, Callable]:
        return {
            "github.search_repos": self.search_repos,
            "github.list_issues": self.list_issues,
            "github.create_issue": self.create_issue,
            "github.get_file": self.get_file,
            "github.list_prs": self.list_prs,
        }

    @tool_schema("github.search_repos", "Search GitHub repositories",
        {"query": {"type": "string", "description": "Search query"},
         "limit": {"type": "integer", "description": "Max results (default 5)"}},
        required=["query"])
    async def search_repos(self, query: str, limit: int = 5) -> str:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/search/repositories", params={"q": query, "per_page": limit}, headers=self._headers)
            r.raise_for_status()
            items = r.json().get("items", [])
        return "\n".join(f"{i['full_name']}: {i.get('description', '')} (★{i['stargazers_count']})" for i in items) or "No results."

    @tool_schema("github.list_issues", "List issues for a GitHub repo",
        {"repo": {"type": "string", "description": "owner/repo"},
         "state": {"type": "string", "description": "open|closed|all"}},
        required=["repo"])
    async def list_issues(self, repo: str, state: str = "open") -> str:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/repos/{repo}/issues", params={"state": state, "per_page": 10}, headers=self._headers)
            r.raise_for_status()
            issues = r.json()
        return "\n".join(f"#{i['number']} [{i['state']}] {i['title']}" for i in issues) or "No issues."

    @tool_schema("github.create_issue", "Create a GitHub issue",
        {"repo": {"type": "string"}, "title": {"type": "string"}, "body": {"type": "string"}},
        required=["repo", "title"])
    async def create_issue(self, repo: str, title: str, body: str = "") -> str:
        if not self._headers.get("Authorization"):
            return "[Error: GitHub token not configured. Run: forgix modules configure github]"
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.post(f"{self._base}/repos/{repo}/issues", json={"title": title, "body": body}, headers=self._headers)
            r.raise_for_status()
            issue = r.json()
        return f"Created issue #{issue['number']}: {issue['html_url']}"

    @tool_schema("github.get_file", "Get file content from a GitHub repo",
        {"repo": {"type": "string"}, "path": {"type": "string"}, "ref": {"type": "string"}},
        required=["repo", "path"])
    async def get_file(self, repo: str, path: str, ref: str = "main") -> str:
        import base64
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/repos/{repo}/contents/{path}", params={"ref": ref}, headers=self._headers)
            if r.status_code == 404:
                return f"[File not found: {path}]"
            r.raise_for_status()
            data = r.json()
        content = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
        return content[:4000]  # limit to 4k chars

    @tool_schema("github.list_prs", "List pull requests for a repo",
        {"repo": {"type": "string"}, "state": {"type": "string"}},
        required=["repo"])
    async def list_prs(self, repo: str, state: str = "open") -> str:
        async with httpx.AsyncClient(timeout=15.0) as c:
            r = await c.get(f"{self._base}/repos/{repo}/pulls", params={"state": state, "per_page": 10}, headers=self._headers)
            r.raise_for_status()
            prs = r.json()
        return "\n".join(f"#{p['number']} {p['title']} ({p['user']['login']})" for p in prs) or "No PRs."
