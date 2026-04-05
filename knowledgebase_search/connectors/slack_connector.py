"""Slack knowledgebase connector."""
from typing import List, Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class SlackConnector:
    """Connector for searching Slack messages."""
    
    def __init__(self, token: str):
        """
        Initialize Slack connector.
        
        Args:
            token: Slack bot token
        """
        self.client = WebClient(token=token)
    
    def search_messages(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search for Slack messages.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of message results with metadata
        """
        try:
            results = self.client.search_messages(query=query, count=limit)
            messages = results.get("messages", {}).get("matches", [])
            return self._format_results(messages)
        except SlackApiError as e:
            raise Exception(f"Slack search failed: {e.response['error']}")
    
    def get_channel_messages(self, channel_id: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search messages in a specific channel."""
        try:
            # Get conversation history
            result = self.client.conversations_history(channel=channel_id, limit=limit)
            messages = result.get("messages", [])
            
            # Filter by query
            filtered = [m for m in messages if query.lower() in m.get("text", "").lower()]
            return self._format_results(filtered)
        except SlackApiError as e:
            raise Exception(f"Slack channel search failed: {e.response['error']}")
    
    def _format_results(self, messages: List[Dict]) -> List[Dict[str, Any]]:
        """Format Slack messages into standardized result format."""
        formatted = []
        for msg in messages:
            formatted.append({
                "source": "slack",
                "title": msg.get("text", "")[:100],
                "url": msg.get("permalink", ""),
                "content": msg.get("text", "")[:500],
                "metadata": {
                    "user": msg.get("user", msg.get("username", "Unknown")),
                    "channel": msg.get("channel", {}).get("name", ""),
                    "timestamp": msg.get("ts", ""),
                    "reactions": len(msg.get("reactions", [])),
                    "replies": msg.get("reply_count", 0),
                }
            })
        return formatted
