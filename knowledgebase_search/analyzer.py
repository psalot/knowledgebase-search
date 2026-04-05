"""AI-powered analyzer for search results."""
from typing import List, Dict, Any
import openai
from openai import OpenAI


class SolutionAnalyzer:
    """Uses AI to analyze search results and provide developer/engineering leader solutions."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the analyzer with OpenAI API.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use (default: gpt-4)
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    def analyze_and_solve(self, query: str, search_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze search results and provide solutions.
        
        Args:
            query: Original search query
            search_results: Results from knowledgebase search
            
        Returns:
            Analysis with solutions, recommendations, and insights
        """
        # Prepare context from search results
        context = self._prepare_context(search_results)
        
        # Create prompt for the AI
        prompt = f"""
You are an experienced engineering leader and developer. Analyze the following search results 
from a knowledgebase (Slack, Confluence, Jira) regarding the query: "{query}"

Search Results Context:
{context}

As an engineering leader, provide:
1. **Problem Analysis**: What issues or questions are being addressed?
2. **Solutions**: Specific, actionable solutions based on the context
3. **Best Practices**: Any engineering best practices that apply
4. **Recommendations**: What the team should do next
5. **Risk Assessment**: Potential risks and how to mitigate them

Be concise but comprehensive. Focus on practical, implementable advice.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert engineering leader providing solutions based on knowledgebase search results."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "query": query,
                "analysis": analysis,
                "search_results_count": len(search_results),
                "sources": list(set(r.get("source") for r in search_results if r.get("source")))
            }
            
        except Exception as e:
            return {
                "error": f"AI analysis failed: {str(e)}",
                "query": query,
                "search_results_count": len(search_results)
            }
    
    def _prepare_context(self, search_results: List[Dict[str, Any]]) -> str:
        """Prepare search results into a readable context string."""
        context_parts = []
        
        for i, result in enumerate(search_results[:10]):  # Limit to top 10 for context
            source = result.get("source", "unknown")
            title = result.get("title", "No title")
            content = result.get("content", "No content")[:500]  # Truncate long content
            
            context_parts.append(f"""
Source {i+1}: {source.upper()}
Title: {title}
Content: {content}
---""")
        
        return "\n".join(context_parts)