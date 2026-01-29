"""新闻解析器模块"""
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse


class NewsParser:
    """新闻解析器类"""
    
    def __init__(self):
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
    
    def _clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 去除首尾空白
        text = text.strip()
        # 限制长度
        if len(text) > 500:
            text = text[:500] + "..."
        
        return text
    
    def _extract_link(self, element, base_url: str) -> Optional[str]:
        """提取链接"""
        if not element:
            return None
        
        # 尝试不同的属性
        for attr in ['href', 'src', 'data-url']:
            link = element.get(attr)
            if link:
                # 处理相对URL
                if link.startswith('/'):
                    return urljoin(base_url, link)
                elif link.startswith('http'):
                    return link
                else:
                    return urljoin(base_url, link)
        
        return None
    
    def _extract_text(self, element, selector: str) -> Optional[str]:
        """提取文本"""
        if not element or not selector:
            return None
        
        try:
            if selector.startswith('.'):
                # CSS类选择器
                result = element.select_one(selector)
            elif selector.startswith('#'):
                # ID选择器
                result = element.select_one(selector)
            else:
                # 其他选择器
                result = element.select_one(selector)
            
            if result:
                return self._clean_text(result.get_text())
        except Exception as e:
            self.logger.warning(f"提取文本失败: {e}")
        
        return None
    
    def parse_source(self, source_data: Dict[str, Any], source_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """解析单个新闻源"""
        name = source_data.get('name', 'Unknown')
        url = source_data.get('url', '')
        content = source_data.get('content', '')
        category = source_data.get('category', 'unknown')
        
        if not content:
            self.logger.warning(f"新闻源 '{name}' 没有内容")
            return []
        
        try:
            soup = BeautifulSoup(content, 'html.parser')
            items = []
            
            # 获取选择器配置
            item_selector = source_config.get('selector')
            link_selector = source_config.get('link_selector')
            title_selector = source_config.get('title_selector')
            desc_selector = source_config.get('desc_selector')
            
            if not item_selector:
                self.logger.warning(f"新闻源 '{name}' 没有配置选择器")
                return []
            
            # 查找所有新闻项
            elements = soup.select(item_selector)
            self.logger.info(f"在 '{name}' 中找到 {len(elements)} 个新闻项")
            
            for element in elements[:20]:  # 限制每源最多20条
                try:
                    # 提取链接
                    link_element = element.select_one(link_selector) if link_selector else element
                    link = self._extract_link(link_element, url)
                    
                    # 提取标题
                    title = self._extract_text(element, title_selector) if title_selector else None
                    
                    # 提取描述
                    description = self._extract_text(element, desc_selector) if desc_selector else None
                    
                    # 如果没有标题或链接，跳过
                    if not title or not link:
                        continue
                    
                    # 生成唯一ID
                    item_id = f"{name}_{hash(link)}_{hash(title)}"
                    
                    item = {
                        'id': item_id,
                        'title': title,
                        'link': link,
                        'description': description or title,
                        'source': name,
                        'category': category,
                        'published_at': source_data.get('fetched_at'),
                        'fetched_at': source_data.get('fetched_at')
                    }
                    
                    items.append(item)
                    
                except Exception as e:
                    self.logger.warning(f"解析新闻项失败: {e}")
                    continue
            
            self.logger.info(f"成功解析 '{name}': {len(items)} 条新闻")
            return items
            
        except Exception as e:
            self.logger.error(f"解析新闻源 '{name}' 失败: {e}")
            return []
    
    def parse_all(self, sources_data: List[Dict[str, Any]], sources_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """解析所有新闻源"""
        all_items = []
        
        for source_data in sources_data:
            source_name = source_data.get('name')
            
            # 查找对应的配置
            source_config = None
            for config in sources_config:
                if config.get('name') == source_name:
                    source_config = config
                    break
            
            if not source_config:
                self.logger.warning(f"未找到新闻源 '{source_name}' 的配置")
                continue
            
            items = self.parse_source(source_data, source_config)
            all_items.extend(items)
        
        return all_items
    
    def parse_category_data(self, category_data: Dict[str, Any], config: Any) -> Dict[str, List[Dict[str, Any]]]:
        """解析分类数据"""
        results = {}
        
        for category, sources_data in category_data.items():
            if not sources_data:
                results[category] = []
                continue
            
            # 获取该分类的新闻源配置
            sources_config = config.get_enabled_sources(category)
            
            # 解析该分类的所有新闻
            items = self.parse_all(sources_data, sources_config)
            results[category] = items
        
        return results
    
    def deduplicate_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """去重新闻项"""
        seen_links = set()
        unique_items = []
        
        for item in items:
            link = item.get('link')
            if link and link not in seen_links:
                seen_links.add(link)
                unique_items.append(item)
        
        self.logger.info(f"去重前: {len(items)} 条，去重后: {len(unique_items)} 条")
        return unique_items
    
    def filter_by_time(self, items: List[Dict[str, Any]], hours: int = 24) -> List[Dict[str, Any]]:
        """按时间过滤新闻"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        filtered_items = []
        
        for item in items:
            try:
                published_str = item.get('published_at')
                if published_str:
                    published_dt = datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                    if published_dt.timestamp() >= cutoff_time:
                        filtered_items.append(item)
            except:
                # 如果解析时间失败，保留该项
                filtered_items.append(item)
        
        self.logger.info(f"时间过滤前: {len(items)} 条，过滤后: {len(filtered_items)} 条")
        return filtered_items
    
    def sort_items(self, items: List[Dict[str, Any]], sort_by: str = 'published_at') -> List[Dict[str, Any]]:
        """排序新闻项"""
        def get_sort_key(item):
            if sort_by == 'published_at':
                try:
                    published_str = item.get('published_at')
                    if published_str:
                        return datetime.fromisoformat(published_str.replace('Z', '+00:00'))
                except:
                    pass
            return datetime.now()
        
        return sorted(items, key=get_sort_key, reverse=True)