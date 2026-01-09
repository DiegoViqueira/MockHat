"""Tools"""
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun


duckduckgo_search_tool = DuckDuckGoSearchResults(
    num_results=10, handle_tool_error=True)

wikipedia_search_tool = WikipediaQueryRun(
    api_wrapper=WikipediaAPIWrapper(),
    num_results=10,
    handle_tool_error=True
)
