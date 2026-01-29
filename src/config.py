"""配置管理模块"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, List


class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def get_schedule(self) -> List[str]:
        """获取调度配置"""
        return self.config.get('schedule', [])
    
    def get_news_sources(self, category: str = None) -> Dict[str, List[Dict]]:
        """获取新闻源配置"""
        sources = self.config.get('news_sources', {})
        if category:
            return sources.get(category, [])
        return sources
    
    def get_enabled_sources(self, category: str) -> List[Dict]:
        """获取启用的新闻源"""
        sources = self.get_news_sources(category)
        return [source for source in sources if source.get('enabled', True)]
    
    def get_rss_config(self) -> Dict[str, Any]:
        """获取RSS配置"""
        return self.config.get('rss', {})
    
    def get_html_config(self) -> Dict[str, Any]:
        """获取HTML配置"""
        return self.config.get('html', {})
    
    def get_storage_config(self) -> Dict[str, Any]:
        """获取存储配置"""
        return self.config.get('storage', {})
    
    def get_fetcher_config(self) -> Dict[str, Any]:
        """获取抓取器配置"""
        return self.config.get('fetcher', {})
    
    def get_notifications_config(self) -> Dict[str, Any]:
        """获取通知配置"""
        return self.config.get('notifications', {})
    
    def get_logging_config(self) -> Dict[str, Any]:
        """获取日志配置"""
        return self.config.get('logging', {})
    
    def get_categories(self) -> List[str]:
        """获取所有分类"""
        return list(self.config.get('news_sources', {}).keys())
    
    def get_output_dirs(self) -> Dict[str, str]:
        """获取输出目录配置"""
        rss_config = self.get_rss_config()
        html_config = self.get_html_config()
        storage_config = self.get_storage_config()
        
        return {
            'rss': rss_config.get('output_dir', 'rss'),
            'html': html_config.get('output_dir', 'docs'),
            'data': storage_config.get('data_dir', 'data'),
            'logs': self.get_logging_config().get('file', 'logs/news-aggregator.log').split('/')[0]
        }
    
    def create_directories(self):
        """创建必要的输出目录"""
        dirs = self.get_output_dirs()
        
        for dir_name, dir_path in dirs.items():
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {dir_path}")
    
    def validate(self) -> bool:
        """验证配置有效性"""
        try:
            # 检查必要配置
            assert 'news_sources' in self.config, "缺少 news_sources 配置"
            assert 'rss' in self.config, "缺少 rss 配置"
            assert 'html' in self.config, "缺少 html 配置"
            
            # 检查分类配置
            categories = self.get_categories()
            assert len(categories) > 0, "至少需要配置一个新闻分类"
            
            # 检查每个分类的新闻源
            for category in categories:
                sources = self.get_news_sources(category)
                assert len(sources) > 0, f"分类 '{category}' 没有配置新闻源"
                
                for source in sources:
                    assert 'name' in source, f"新闻源缺少 name 字段"
                    assert 'url' in source, f"新闻源 '{source.get('name')}' 缺少 url 字段"
            
            return True
            
        except AssertionError as e:
            print(f"配置验证失败: {e}")
            return False
        except Exception as e:
            print(f"配置验证异常: {e}")
            return False
    
    def reload(self):
        """重新加载配置"""
        self.config = self._load_config()
        print("配置已重新加载")