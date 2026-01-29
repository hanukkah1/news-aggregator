"""工具函数模块"""
import json
from typing import Dict, Any, List
from pathlib import Path
import logging


class NewsUtils:
    """工具类"""
    
    @staticmethod
    def load_json_file(filepath: str) -> Dict[str, Any]:
        """加载JSON文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"加载JSON文件失败 {filepath}: {e}")
            return {}
    
    @staticmethod
    def save_json_file(data: Dict[str, Any], filepath: str, indent: int = 2):
        """保存JSON文件"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            return True
        except Exception as e:
            logging.error(f"保存JSON文件失败 {filepath}: {e}")
            return False
    
    @staticmethod
    def get_latest_data_file(data_dir: str = "data") -> str:
        """获取最新的数据文件"""
        data_path = Path(data_dir)
        if not data_path.exists():
            return ""
        
        json_files = list(data_path.glob("news_data_*.json"))
        if not json_files:
            return ""
        
        # 按修改时间排序，取最新的
        latest_file = max(json_files, key=lambda x: x.stat().st_mtime)
        return str(latest_file)
    
    @staticmethod
    def format_stats(stats: Dict[str, Any]) -> str:
        """格式化统计信息"""
        if not stats:
            return "暂无统计信息"
        
        output = []
        output.append("=" * 50)
        output.append("新闻聚合器统计信息")
        output.append("=" * 50)
        
        if 'timestamp' in stats:
            output.append(f"更新时间: {stats['timestamp']}")
        
        if 'total_items' in stats:
            output.append(f"新闻总数: {stats['total_items']}")
        
        if 'categories' in stats:
            output.append("分类统计:")
            for cat, count in stats['categories'].items():
                category_names = {'tech': '科技', 'finance': '财经', 'entertainment': '娱乐'}
                cat_name = category_names.get(cat, cat)
                output.append(f"  {cat_name}: {count} 条")
        
        if 'rss_files' in stats:
            output.append(f"RSS文件: {stats['rss_files']} 个")
        
        if 'html_pages' in stats:
            output.append(f"HTML页面: {stats['html_pages']} 个")
        
        output.append("=" * 50)
        
        return "\n".join(output)
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """验证URL格式"""
        from urllib.parse import urlparse
        
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    @staticmethod
    def extract_domain(url: str) -> str:
        """提取域名"""
        from urllib.parse import urlparse
        
        try:
            result = urlparse(url)
            return result.netloc
        except:
            return "Unknown"
    
    @staticmethod
    def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
        """截断文本"""
        if not text:
            return ""
        
        if len(text) <= max_length:
            return text
        
        return text[:max_length - len(suffix)] + suffix
    
    @staticmethod
    def clean_html(text: str) -> str:
        """清理HTML标签"""
        import re
        
        if not text:
            return ""
        
        # 移除HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        # 移除多余的空白字符
        text = re.sub(r'\s+', ' ', text)
        # 去除首尾空白
        return text.strip()
    
    @staticmethod
    def get_file_size(filepath: str) -> str:
        """获取文件大小"""
        try:
            size = Path(filepath).stat().st_size
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size < 1024.0:
                    return f"{size:.2f} {unit}"
                size /= 1024.0
            return f"{size:.2f} TB"
        except:
            return "Unknown"
    
    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> List[str]:
        """列出目录下的文件"""
        try:
            path = Path(directory)
            if not path.exists():
                return []
            
            return [str(f) for f in path.glob(pattern) if f.is_file()]
        except:
            return []
    
    @staticmethod
    def create_symlink(source: str, target: str):
        """创建符号链接"""
        try:
            source_path = Path(source)
            target_path = Path(target)
            
            if target_path.exists():
                target_path.unlink()
            
            # Windows不支持符号链接，使用复制
            if sys.platform == "win32":
                import shutil
                shutil.copy2(source_path, target_path)
            else:
                target_path.symlink_to(source_path)
            
            return True
        except Exception as e:
            logging.error(f"创建符号链接失败: {e}")
            return False