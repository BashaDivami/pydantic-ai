from pydantic_ai import Tool
import httpx

@Tool
def web_search(query: str) -> str:
    """
    Simple web search tool using DuckDuckGo.
    """
    url = f"https://api.duckduckgo.com/?q={query}&format=json"
    res = httpx.get(url)
    return res.text
