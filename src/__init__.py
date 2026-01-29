"""新闻聚合器主模块"""
from .config import Config
from .fetcher import NewsFetcher
from .parser import NewsParser
from .rss_generator import RSSGenerator
from .html_generator import HTMLGenerator
from .main import main

__version__ = "1.0.0"
__all__ = ["Config", "NewsFetcher", "NewsParser", "RSSGenerator", "HTMLGenerator", "main"]