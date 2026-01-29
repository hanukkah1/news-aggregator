"""RSS订阅源生成器模块"""
from feedgen.feed import FeedGenerator
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import logging


class RSSGenerator:
    """RSS生成器类"""
    
    def __init__(self, config: Any):
        self.config = config
        self.rss_config = config.get_rss_config()
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def create_feed(self, category: str, items: List[Dict[str, Any]]) -> FeedGenerator:
        """创建RSS feed"""
        fg = FeedGenerator()
        
        # 基本信息
        title = f"新闻聚合器 - {category.upper()} 分类"
        description = f"自动聚合的 {category} 分类新闻"
        link = f"https://github.com/{self.config.get('github_repo', 'your-username/news-aggregator')}"
        
        fg.title(title)
        fg.description(description)
        fg.link(href=link, rel='alternate')
        fg.language(self.rss_config.get('language', 'zh-CN'))
        fg.author({'name': self.rss_config.get('author', 'Auto News Aggregator')})
        
        # 添加TTL
        ttl = self.rss_config.get('ttl', 180)
        fg.ttl(ttl)
        
        # 添加分类信息
        fg.category(category)
        
        return fg
    
    def add_entry(self, fg: FeedGenerator, item: Dict[str, Any]):
        """添加RSS条目"""
        fe = fg.add_entry()
        
        title = item.get('title', '无标题')
        link = item.get('link', '')
        description = item.get('description', '')
        published_at = item.get('published_at')
        source = item.get('source', 'Unknown')
        
        fe.title(title)
        fe.link(href=link, rel='alternate')
        fe.description(description)
        fe.source(source)
        
        # 设置发布时间
        if published_at:
            try:
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                fe.pubDate(pub_date)
            except:
                fe.pubDate(datetime.now())
        
        # 添加唯一ID
        item_id = item.get('id')
        if item_id:
            fe.guid(item_id, permalink=False)
        
        # 添加作者信息
        fe.author({'name': source})
    
    def generate_category_rss(self, category: str, items: List[Dict[str, Any]]) -> str:
        """生成单个分类的RSS"""
        if not items:
            self.logger.warning(f"分类 '{category}' 没有新闻项，跳过RSS生成")
            return ""
        
        # 限制条目数量
        max_items = self.rss_config.get('max_items_per_feed', 50)
        limited_items = items[:max_items]
        
        # 创建feed
        fg = self.create_feed(category, limited_items)
        
        # 添加条目
        for item in limited_items:
            self.add_entry(fg, item)
        
        # 生成RSS XML
        rss_feed = fg.rss_str(pretty=True)
        
        self.logger.info(f"生成分类 '{category}' RSS，包含 {len(limited_items)} 条新闻")
        
        return rss_feed
    
    def save_rss(self, rss_feed: str, category: str, output_dir: str = "rss"):
        """保存RSS到文件"""
        if not rss_feed:
            return
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 生成文件名
        filename = f"{category.lower()}.xml"
        filepath = output_path / filename
        
        # 保存文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rss_feed)
        
        self.logger.info(f"RSS已保存到: {filepath}")
        
        return str(filepath)
    
    def generate_all_rss(self, categorized_items: Dict[str, List[Dict[str, Any]]], output_dir: str = "rss") -> Dict[str, str]:
        """生成所有分类的RSS"""
        output_files = {}
        
        for category, items in categorized_items.items():
            if not items:
                continue
            
            rss_feed = self.generate_category_rss(category, items)
            if rss_feed:
                filepath = self.save_rss(rss_feed, category, output_dir)
                if filepath:
                    output_files[category] = filepath
        
        self.logger.info(f"RSS生成完成，共生成 {len(output_files)} 个文件")
        return output_files
    
    def generate_index_rss(self, all_items: List[Dict[str, Any]], output_dir: str = "rss") -> str:
        """生成总RSS（包含所有分类）"""
        if not all_items:
            self.logger.warning("没有新闻项，跳过总RSS生成")
            return ""
        
        # 按时间排序
        sorted_items = sorted(
            all_items,
            key=lambda x: x.get('published_at', ''),
            reverse=True
        )
        
        # 限制条目数量
        max_items = self.rss_config.get('max_items_per_feed', 50)
        limited_items = sorted_items[:max_items]
        
        # 创建feed
        fg = FeedGenerator()
        fg.title("新闻聚合器 - 所有分类")
        fg.description("自动聚合的所有分类新闻")
        fg.link(href="https://github.com/your-username/news-aggregator", rel='alternate')
        fg.language(self.rss_config.get('language', 'zh-CN'))
        fg.author({'name': self.rss_config.get('author', 'Auto News Aggregator')})
        fg.ttl(self.rss_config.get('ttl', 180))
        
        # 添加条目
        for item in limited_items:
            self.add_entry(fg, item)
        
        # 生成RSS XML
        rss_feed = fg.rss_str(pretty=True)
        
        # 保存文件
        filepath = self.save_rss(rss_feed, "all", output_dir)
        
        self.logger.info(f"总RSS生成完成，包含 {len(limited_items)} 条新闻")
        
        return filepath if filepath else ""
    
    def generate_feed_urls(self, base_url: str, categories: List[str]) -> Dict[str, str]:
        """生成RSS订阅链接"""
        feed_urls = {}
        
        for category in categories:
            feed_urls[category] = f"{base_url.rstrip('/')}/{category.lower()}.xml"
        
        # 添加总RSS
        feed_urls['all'] = f"{base_url.rstrip('/')}/all.xml"
        
        return feed_urls