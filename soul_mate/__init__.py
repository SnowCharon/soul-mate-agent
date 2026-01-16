"""
灵魂伴侣 - 个性化阅读推荐Agent
"""

from .agent import SoulMateAgent
from .user_profile import UserProfile
from .llm_client import LLMClient
from .content_fetcher import ContentFetcher

__version__ = "1.0.0"
__all__ = ["SoulMateAgent", "UserProfile", "LLMClient", "ContentFetcher"]
