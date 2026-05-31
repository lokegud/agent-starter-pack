"""
Forgix web search skill — DuckDuckGo, no API key required.

Uses the DuckDuckGo HTML/Lite endpoints. Results pass through PromptGuard
upstream (wrapped by the agent's wrap_external).
"""
from __future__ import annotations

import re
from html import unescape

import httpx

from forgix.modules.base import tool_schema


@tool_schema(
    "skill.web_search",
    "Search the web via DuckDuckGo. Returns top results with titles and snippets.",
    {"query": {"type": "string", "description": "Search query"},
     "limit": {"type": "integer", "description": "Max results (default 5)"}},
    required=["query"],
)
async def web_search(query: str, limit: int = 5) -> str:
    """Search DuckDuckGo and return formatted results."""
    try:
        async with httpx.AsyncClient(timeout=15.0, follow_redirects=True) as c:
            r = await c.post(
                "https://lite.duckduckgo.com/lite/",
                data={"q": query},
                headers={"User-Agent": "Mozilla/5.0 (compatible; Forgix/0.1)"},
            )
            r.raise_for_status()
            html = r.text
    except Exception as e:
        return f"[Search error: {e}]"

    # Parse lite.duckduckgo.com results
    results = []
    # Links appear as <a rel="nofollow" href="..." class='result-link'>title</a>
    link_pattern = re.compile(r'<a[^>]*class=["\']result-link["\'][^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.S)
    snippet_pattern = re.compile(r'class=["\']result-snippet["\'][^>]*>(.*?)</td>', re.S)

    links = link_pattern.findall(html)
    snippets = snippet_pattern.findall(html)

    def clean(text: str) -> str:
        return unescape(re.sub(r"<[^>]+>", "", text)).strip()

    for i, (url, title) in enumerate(links[:limit]):
        snippet = clean(snippets[i]) if i < len(snippets) else ""
        results.append(f"{i+1}. {clean(title)}\n   {url}\n   {snippet[:200]}")

    if not results:
        # Fallback to instant-answer API
        try:
            async with httpx.AsyncClient(timeout=10.0) as c:
                r = await c.get("https://api.duckduckgo.com/",
                    params={"q": query, "format": "json", "no_html": 1})
                data = r.json()
            abstract = data.get("AbstractText") or data.get("Answer")
            if abstract:
                return f"{abstract}\nSource: {data.get('AbstractURL', '')}"
        except Exception:
            pass
        return f"No results found for '{query}'."

    return "\n\n".join(results)
