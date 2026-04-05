"""Main search functionality for knowledgebase."""
from typing import List, Dict, Any, Optional
from .connectors.slack_connector import SlackConnector
from .connectors.confluence_connector import ConfluenceConnector
from .connectors.jira_connector import JiraConnector
from .analyzer import SolutionAnalyzer


class KnowledgebaseSearch:
    """Main class for searching across multiple knowledge sources."""
    
    def __init__(self, slack_token: Optional[str] = None, confluence_url: Optional[str] = None,
                 confluence_username: Optional[str] = None, confluence_password: Optional[str] = None,
                 jira_url: Optional[str] = None, jira_username: Optional[str] = None,
                 jira_password: Optional[str] = None, openai_api_key: Optional[str] = None):
        """
        Initialize search with available connectors.
        
        Args:
            slack_token: Slack bot token
            confluence_url: Confluence base URL
            confluence_username: Confluence username
            confluence_password: Confluence password/token
            jira_url: Jira base URL
            jira_username: Jira username
            jira_password: Jira password/token
            openai_api_key: OpenAI API key for AI analysis
        """
        self.connectors = []
        
        if slack_token:
            self.connectors.append(SlackConnector(slack_token))
        
        if confluence_url and confluence_username and confluence_password:
            self.connectors.append(ConfluenceConnector(confluence_url, confluence_username, confluence_password))
        
        if jira_url and jira_username and jira_password:
            self.connectors.append(JiraConnector(jira_url, jira_username, jira_password))
        
        self.analyzer = SolutionAnalyzer(openai_api_key) if openai_api_key else None
    
    def search(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search across all configured knowledge sources.
        
        Args:
            query: Search query
            limit: Maximum results per source
            
        Returns:
            Aggregated search results
        """
        all_results = []
        
        for connector in self.connectors:
            try:
                if isinstance(connector, SlackConnector):
                    results = connector.search_messages(query, limit)
                elif isinstance(connector, ConfluenceConnector):
                    results = connector.search_pages(query, limit)
                elif isinstance(connector, JiraConnector):
                    results = connector.search_issues(query, limit)
                else:
                    continue
                
                all_results.extend(results)
            except Exception as e:
                # Log error but continue with other connectors
                print(f"Error searching {type(connector).__name__}: {e}")
        
        # Sort by relevance (simple implementation - could be improved)
        # For now, just return all results
        return all_results[:limit * len(self.connectors)]  # Allow more results if multiple sources
    
    def search_and_analyze(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search across all sources and provide AI-powered analysis and solutions.
        
        Args:
            query: Search query
            limit: Maximum results per source
            
        Returns:
            Dictionary with search results and AI analysis
        """
        # First, perform the search
        search_results = self.search(query, limit)
        
        # If analyzer is available, get AI analysis
        if self.analyzer:
            analysis = self.analyzer.analyze_and_solve(query, search_results)
            return {
                "search_results": search_results,
                "ai_analysis": analysis
            }
        else:
            return {
                "search_results": search_results,
                "ai_analysis": None,
                "message": "No OpenAI API key provided - analysis unavailable"
            }