# knowledgebase-search
A Python tool to search and aggregate answers from Confluence, Jira, and Slack, with AI-powered analysis and solutions.

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool:

```bash
python cli.py "your search query" --slack-token YOUR_SLACK_TOKEN --confluence-url YOUR_CONFLUENCE_URL --confluence-username USER --confluence-password PASS --jira-url YOUR_JIRA_URL --jira-username USER --jira-password PASS
```

### AI-Powered Analysis

For developer/engineering leader solutions, include AI analysis:

```bash
python cli.py "database performance issue" --slack-token YOUR_TOKEN --openai-api-key YOUR_OPENAI_KEY --analyze
```

This will:
- Search across all configured knowledge sources
- Use GPT-4 to analyze results
- Provide actionable solutions, best practices, and recommendations

## Configuration

Provide API tokens and credentials for the sources you want to search. All parameters are optional - only configure the sources you have access to.

For AI analysis, provide an OpenAI API key.
