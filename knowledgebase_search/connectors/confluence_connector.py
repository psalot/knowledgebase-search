"""Confluence knowledgebase connector."""
from typing import List, Dict, Any
from atlassian import Confluence


class ConfluenceConnector:
    """Connector for searching Confluence pages."""
    
    def __init__(self, url: str, username: str, password: str):
        """
        Initialize Confluence connector.
        
        Args:
            url: Confluence base URL
            username: Username
            password: Password or API token
        """
        self.confluence = Confluence(url=url, username=username, password=password)
    
    def search_pages(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for Confluence pages."""
        try:
            results = self.confluence.cql(query=f"text ~ \"{query}\"", limit=limit)
            pages = results.get("results", [])
            return self._format_results(pages)
        except Exception as e:
            raise Exception(f"Confluence search failed: {str(e)}")
    
    def _format_results(self, pages: List[Dict]) -> List[Dict[str, Any]]:
        """Format Confluence pages into standardized result format."""
        formatted = []
        for page in pages:
            formatted.append({
                "title": page.get("title", ""),
                "content": page.get("body", {}).get("storage", {}).get("value", ""),
                "url": page.get("_links", {}).get("webui", ""),
                "source": "confluence",
                "metadata": {
                    "id": page.get("id"),
                    "space": page.get("space", {}).get("name"),
                    "last_modified": page.get("version", {}).get("when")
                }
            })
        return formatted