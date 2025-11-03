"""Modern research assistant powered by GPT-5 and Chrome DevTools."""

from .gpt import GPTResearchAgent
from .browser import ChromeDevToolsSession, SearchResult, PageInsights
from .storage import ResearchStorage

__all__ = [
    "GPTResearchAgent",
    "ChromeDevToolsSession",
    "SearchResult",
    "PageInsights",
    "ResearchStorage",
]

