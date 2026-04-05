"""Jira knowledgebase connector."""
from typing import List, Dict, Any
from atlassian import Jira


class JiraConnector:
    """Connector for searching Jira issues."""
    
    def __init__(self, url: str, username: str, password: str):
        """
        Initialize Jira connector.
        
        Args:
            url: Jira base URL
            username: Username
            password: Password or API token
        """
        self.jira = Jira(url=url, username=username, password=password)
    
    def search_issues(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for Jira issues."""
        try:
            jql = f"text ~ \"{query}\""
            results = self.jira.jql(jql, limit=limit)
            issues = results.get("issues", [])
            return self._format_results(issues)
        except Exception as e:
            raise Exception(f"Jira search failed: {str(e)}")
    
    def _format_results(self, issues: List[Dict]) -> List[Dict[str, Any]]:
        """Format Jira issues into standardized result format."""
        formatted = []
        for issue in issues:
            fields = issue.get("fields", {})
            formatted.append({
                "title": fields.get("summary", ""),
                "content": fields.get("description", ""),
                "url": issue.get("self", ""),
                "source": "jira",
                "metadata": {
                    "key": issue.get("key"),
                    "status": fields.get("status", {}).get("name"),
                    "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
                    "created": fields.get("created")
                }
            })
        return formatted