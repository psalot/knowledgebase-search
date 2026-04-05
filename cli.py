#!/usr/bin/env python3
"""CLI for knowledgebase search."""
import argparse
import json
from knowledgebase_search.search import KnowledgebaseSearch


def main():
    parser = argparse.ArgumentParser(description="Search knowledgebase across Slack, Confluence, and Jira")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--slack-token", help="Slack bot token")
    parser.add_argument("--confluence-url", help="Confluence base URL")
    parser.add_argument("--confluence-username", help="Confluence username")
    parser.add_argument("--confluence-password", help="Confluence password/token")
    parser.add_argument("--jira-url", help="Jira base URL")
    parser.add_argument("--jira-username", help="Jira username")
    parser.add_argument("--jira-password", help="Jira password/token")
    parser.add_argument("--openai-api-key", help="OpenAI API key for AI analysis")
    parser.add_argument("--limit", type=int, default=10, help="Maximum results per source")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--analyze", action="store_true", help="Include AI-powered analysis and solutions")
    
    args = parser.parse_args()
    
    search = KnowledgebaseSearch(
        slack_token=args.slack_token,
        confluence_url=args.confluence_url,
        confluence_username=args.confluence_username,
        confluence_password=args.confluence_password,
        jira_url=args.jira_url,
        jira_username=args.jira_username,
        jira_password=args.jira_password,
        openai_api_key=args.openai_api_key
    )
    
    if args.analyze:
        result = search.search_and_analyze(args.query, args.limit)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            # Print search results
            print("=== SEARCH RESULTS ===")
            for res in result["search_results"]:
                print(f"Source: {res.get('source', 'unknown')}")
                print(f"Title: {res.get('title', 'No title')}")
                print(f"URL: {res.get('url', 'No URL')}")
                print(f"Content: {res.get('content', 'No content')[:200]}...")
                print("-" * 50)
            
            # Print AI analysis
            print("\n=== AI ANALYSIS & SOLUTIONS ===")
            if result["ai_analysis"]:
                if "error" in result["ai_analysis"]:
                    print(f"Error: {result['ai_analysis']['error']}")
                else:
                    print(result["ai_analysis"]["analysis"])
            else:
                print(result.get("message", "Analysis not available"))
    else:
        results = search.search(args.query, args.limit)
        
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for result in results:
                print(f"Source: {result.get('source', 'unknown')}")
                print(f"Title: {result.get('title', 'No title')}")
                print(f"URL: {result.get('url', 'No URL')}")
                print(f"Content: {result.get('content', 'No content')[:200]}...")
                print("-" * 50)


if __name__ == "__main__":
    main()