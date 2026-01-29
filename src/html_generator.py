"""HTML页面生成器模块"""
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path
import logging
import json


class HTMLGenerator:
    """HTML生成器类"""
    
    def __init__(self, config: Any):
        self.config = config
        self.html_config = config.get_html_config()
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
    
    def _get_css_styles(self) -> str:
        """获取CSS样式"""
        theme = self.html_config.get('theme', 'modern')
        
        if theme == 'dark':
            return """
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: #1a1a1a; 
                    color: #e0e0e0; 
                    margin: 0; 
                    padding: 20px;
                    line-height: 1.6;
                }
                .container { max-width: 1200px; margin: 0 auto; }
                .header { 
                    background: #2d2d2d; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 20px;
                    text-align: center;
                }
                .header h1 { margin: 0; color: #fff; }
                .header p { margin: 5px 0 0; color: #aaa; }
                .nav { 
                    background: #2d2d2d; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin-bottom: 20px;
                    display: flex; 
                    gap: 10px; 
                    flex-wrap: wrap;
                }
                .nav a { 
                    color: #4a9eff; 
                    text-decoration: none; 
                    padding: 8px 15px; 
                    background: #3d3d3d; 
                    border-radius: 5px;
                    transition: background 0.3s;
                }
                .nav a:hover { background: #4d4d4d; }
                .category-section { 
                    background: #2d2d2d; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 20px;
                }
                .category-title { 
                    color: #fff; 
                    border-bottom: 2px solid #4a9eff; 
                    padding-bottom: 10px; 
                    margin-bottom: 15px;
                }
                .news-item { 
                    background: #3d3d3d; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin-bottom: 10px;
                    border-left: 4px solid #4a9eff;
                }
                .news-item:hover { background: #454545; }
                .news-title { 
                    font-size: 18px; 
                    font-weight: 600; 
                    margin-bottom: 8px;
                }
                .news-title a { 
                    color: #fff; 
                    text-decoration: none;
                }
                .news-title a:hover { color: #4a9eff; }
                .news-meta { 
                    font-size: 12px; 
                    color: #aaa; 
                    margin-bottom: 8px;
                }
                .news-description { 
                    color: #ccc; 
                    font-size: 14px;
                    line-height: 1.5;
                }
                .news-source { 
                    color: #4a9eff; 
                    font-weight: 500;
                }
                .footer { 
                    text-align: center; 
                    color: #666; 
                    padding: 20px; 
                    margin-top: 30px;
                    font-size: 12px;
                }
                .stats { 
                    background: #3d3d3d; 
                    padding: 15px; 
                    border-radius: 6px; 
                    margin-bottom: 20px;
                    display: flex; 
                    gap: 20px; 
                    flex-wrap: wrap;
                }
                .stat-item { 
                    flex: 1; 
                    min-width: 150px; 
                    text-align: center;
                }
                .stat-value { 
                    font-size: 24px; 
                    font-weight: bold; 
                    color: #4a9eff;
                }
                .stat-label { 
                    font-size: 12px; 
                    color: #aaa;
                }
            """
        elif theme == 'minimal':
            return """
                body { 
                    font-family: Georgia, serif;
                    background: #fff; 
                    color: #333; 
                    margin: 0; 
                    padding: 40px 20px;
                    line-height: 1.8;
                }
                .container { max-width: 800px; margin: 0 auto; }
                .header { margin-bottom: 30px; text-align: center; }
                .header h1 { font-size: 32px; margin: 0 0 10px; }
                .header p { color: #666; margin: 0; }
                .nav { margin-bottom: 30px; text-align: center; }
                .nav a { 
                    color: #333; 
                    text-decoration: none; 
                    margin: 0 10px; 
                    font-size: 14px;
                    text-transform: uppercase;
                    letter-spacing: 1px;
                }
                .category-section { margin-bottom: 40px; }
                .category-title { 
                    font-size: 24px; 
                    border-bottom: 1px solid #ddd; 
                    padding-bottom: 10px; 
                    margin-bottom: 20px;
                }
                .news-item { margin-bottom: 25px; }
                .news-title { font-size: 18px; margin-bottom: 5px; }
                .news-title a { color: #333; text-decoration: none; }
                .news-title a:hover { text-decoration: underline; }
                .news-meta { font-size: 12px; color: #999; margin-bottom: 5px; }
                .news-description { font-size: 14px; color: #555; }
                .footer { 
                    text-align: center; 
                    color: #999; 
                    margin-top: 40px; 
                    font-size: 12px;
                    border-top: 1px solid #eee; 
                    padding-top: 20px;
                }
            """
        else:  # modern (default)
            return """
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0; 
                    padding: 20px;
                    min-height: 100vh;
                }
                .container { 
                    max-width: 1200px; 
                    margin: 0 auto; 
                    background: white; 
                    border-radius: 12px; 
                    overflow: hidden;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }
                .header { 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; 
                    padding: 30px; 
                    text-align: center;
                }
                .header h1 { 
                    margin: 0; 
                    font-size: 32px; 
                    font-weight: 700;
                    letter-spacing: -0.5px;
                }
                .header p { 
                    margin: 10px 0 0; 
                    opacity: 0.9; 
                    font-size: 14px;
                }
                .nav { 
                    background: #f8f9fa; 
                    padding: 15px 30px; 
                    display: flex; 
                    gap: 10px; 
                    flex-wrap: wrap;
                    border-bottom: 1px solid #e9ecef;
                }
                .nav a { 
                    color: #667eea; 
                    text-decoration: none; 
                    padding: 8px 16px; 
                    background: white; 
                    border-radius: 20px;
                    font-weight: 500;
                    font-size: 14px;
                    transition: all 0.3s;
                    border: 1px solid #e9ecef;
                }
                .nav a:hover { 
                    background: #667eea; 
                    color: white; 
                    transform: translateY(-2px);
                }
                .nav a.active { 
                    background: #667eea; 
                    color: white;
                }
                .stats { 
                    background: #f8f9fa; 
                    padding: 20px 30px; 
                    display: flex; 
                    gap: 20px; 
                    flex-wrap: wrap;
                    border-bottom: 1px solid #e9ecef;
                }
                .stat-item { 
                    flex: 1; 
                    min-width: 120px; 
                    text-align: center;
                    background: white; 
                    padding: 15px; 
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                }
                .stat-value { 
                    font-size: 26px; 
                    font-weight: 700; 
                    color: #667eea;
                    display: block;
                }
                .stat-label { 
                    font-size: 12px; 
                    color: #6c757d; 
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-top: 5px;
                    display: block;
                }
                .category-section { 
                    padding: 30px;
                    border-bottom: 1px solid #e9ecef;
                }
                .category-section:last-child { border-bottom: none; }
                .category-title { 
                    font-size: 24px; 
                    font-weight: 700; 
                    color: #212529;
                    margin-bottom: 20px;
                    display: flex; 
                    align-items: center; 
                    gap: 10px;
                }
                .category-title::before {
                    content: '';
                    width: 4px; 
                    height: 24px; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 2px;
                }
                .news-item { 
                    background: white; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin-bottom: 15px;
                    border: 1px solid #e9ecef;
                    transition: all 0.3s;
                    position: relative;
                    overflow: hidden;
                }
                .news-item::before {
                    content: '';
                    position: absolute;
                    left: 0; top: 0; bottom: 0;
                    width: 4px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    opacity: 0;
                    transition: opacity 0.3s;
                }
                .news-item:hover { 
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
                    border-color: #667eea;
                }
                .news-item:hover::before { opacity: 1; }
                .news-title { 
                    font-size: 18px; 
                    font-weight: 600; 
                    margin-bottom: 8px;
                    line-height: 1.4;
                }
                .news-title a { 
                    color: #212529; 
                    text-decoration: none;
                    transition: color 0.2s;
                }
                .news-title a:hover { 
                    color: #667eea; 
                    text-decoration: underline;
                }
                .news-meta { 
                    font-size: 12px; 
                    color: #6c757d; 
                    margin-bottom: 8px;
                    display: flex; 
                    gap: 10px; 
                    flex-wrap: wrap;
                }
                .news-source { 
                    background: #e7eaff; 
                    color: #667eea; 
                    padding: 2px 8px; 
                    border-radius: 10px;
                    font-weight: 500;
                }
                .news-time { 
                    color: #6c757d;
                }
                .news-description { 
                    color: #495057; 
                    font-size: 14px;
                    line-height: 1.6;
                    margin-top: 8px;
                }
                .footer { 
                    text-align: center; 
                    color: #6c757d; 
                    padding: 30px;
                    font-size: 12px;
                    background: #f8f9fa;
                    border-top: 1px solid #e9ecef;
                }
                .footer a { 
                    color: #667eea; 
                    text-decoration: none;
                }
                .timestamp { 
                    font-size: 11px; 
                    color: #adb5bd; 
                    margin-top: 10px;
                    text-align: center;
                }
            """
    
    def _format_time(self, iso_time: str) -> str:
        """格式化时间"""
        try:
            dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M')
        except:
            return iso_time
    
    def generate_main_page(self, categorized_items: Dict[str, List[Dict[str, Any]]], 
                          rss_files: Dict[str, str], output_dir: str = "docs") -> str:
        """生成主页面"""
        # 收集所有新闻
        all_items = []
        for items in categorized_items.values():
            all_items.extend(items)
        
        # 按时间排序
        all_items.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        
        # 统计信息
        stats = {
            'total': len(all_items),
            'tech': len(categorized_items.get('tech', [])),
            'finance': len(categorized_items.get('finance', [])),
            'entertainment': len(categorized_items.get('entertainment', [])),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 生成HTML
        html = self._generate_html(
            title="新闻聚合器 - 首页",
            stats=stats,
            categorized_items=categorized_items,
            rss_files=rss_files,
            is_main=True
        )
        
        # 保存文件
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / "index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.logger.info(f"主页面已生成: {filepath}")
        return str(filepath)
    
    def generate_category_pages(self, categorized_items: Dict[str, List[Dict[str, Any]]], 
                               rss_files: Dict[str, str], output_dir: str = "docs") -> Dict[str, str]:
        """生成分类页面"""
        output_files = {}
        
        for category, items in categorized_items.items():
            if not items:
                continue
            
            # 按时间排序
            sorted_items = sorted(items, key=lambda x: x.get('published_at', ''), reverse=True)
            
            # 统计信息
            stats = {
                'total': len(sorted_items),
                'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 生成HTML
            html = self._generate_html(
                title=f"新闻聚合器 - {category.upper()} 分类",
                stats=stats,
                categorized_items={category: sorted_items},
                rss_files=rss_files,
                category=category,
                is_main=False
            )
            
            # 保存文件
            output_path = Path(output_dir) / "category"
            output_path.mkdir(parents=True, exist_ok=True)
            
            filepath = output_path / f"{category.lower()}.html"
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            
            output_files[category] = str(filepath)
            self.logger.info(f"分类页面已生成: {filepath}")
        
        return output_files
    
    def _generate_html(self, title: str, stats: Dict[str, Any], 
                      categorized_items: Dict[str, List[Dict[str, Any]]],
                      rss_files: Dict[str, str], category: str = None, 
                      is_main: bool = False) -> str:
        """生成HTML内容"""
        css_styles = self._get_css_styles()
        
        # 生成导航
        nav_html = self._generate_nav(is_main, category)
        
        # 生成统计信息
        stats_html = self._generate_stats(stats)
        
        # 生成新闻内容
        content_html = self._generate_content(categorized_items, is_main)
        
        # 生成RSS链接
        rss_html = self._generate_rss_links(rss_files, category)
        
        # 生成时间戳
        timestamp_html = f'<div class="timestamp">最后更新: {stats.get("updated_at", "未知")}</div>'
        
        # 完整的HTML
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{css_styles}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 新闻聚合器</h1>
            <p>自动聚合科技、财经、娱乐新闻 | 每日更新</p>
        </div>
        
        {nav_html}
        
        {stats_html}
        
        {rss_html}
        
        {content_html}
        
        {timestamp_html}
        
        <div class="footer">
            <p>Powered by Auto News Aggregator | 
            <a href="https://github.com/your-username/news-aggregator" target="_blank">GitHub</a> | 
            <a href="https://github.com/your-username/news-aggregator/actions" target="_blank">Actions</a></p>
            <p>© {datetime.now().year} 新闻聚合器 | 本页面由GitHub Actions自动生成</p>
        </div>
    </div>
</body>
</html>"""
        
        return html
    
    def _generate_nav(self, is_main: bool, current_category: str = None) -> str:
        """生成导航栏"""
        categories = ['tech', 'finance', 'entertainment']
        category_names = {'tech': '科技', 'finance': '财经', 'entertainment': '娱乐'}
        
        nav_items = []
        
        # 首页链接
        if is_main:
            nav_items.append('<a href="../index.html" class="active">🏠 首页</a>')
        else:
            nav_items.append('<a href="../index.html">🏠 首页</a>')
        
        # 分类链接
        for cat in categories:
            if cat == current_category:
                nav_items.append(f'<a href="{cat}.html" class="active">📊 {category_names[cat]}</a>')
            else:
                nav_items.append(f'<a href="{cat}.html">📊 {category_names[cat]}</a>')
        
        # RSS链接
        nav_items.append('<a href="../rss" target="_blank">📡 RSS订阅</a>')
        
        return f'<div class="nav">{" ".join(nav_items)}</div>'
    
    def _generate_stats(self, stats: Dict[str, Any]) -> str:
        """生成统计信息"""
        if not stats:
            return ""
        
        stats_items = []
        
        if 'total' in stats:
            stats_items.append(f"""
                <div class="stat-item">
                    <span class="stat-value">{stats['total']}</span>
                    <span class="stat-label">总新闻数</span>
                </div>
            """)
        
        if 'tech' in stats and stats['tech'] > 0:
            stats_items.append(f"""
                <div class="stat-item">
                    <span class="stat-value">{stats['tech']}</span>
                    <span class="stat-label">科技</span>
                </div>
            """)
        
        if 'finance' in stats and stats['finance'] > 0:
            stats_items.append(f"""
                <div class="stat-item">
                    <span class="stat-value">{stats['finance']}</span>
                    <span class="stat-label">财经</span>
                </div>
            """)
        
        if 'entertainment' in stats and stats['entertainment'] > 0:
            stats_items.append(f"""
                <div class="stat-item">
                    <span class="stat-value">{stats['entertainment']}</span>
                    <span class="stat-label">娱乐</span>
                </div>
            """)
        
        if not stats_items:
            return ""
        
        return f'<div class="stats">{" ".join(stats_items)}</div>'
    
    def _generate_content(self, categorized_items: Dict[str, List[Dict[str, Any]]], is_main: bool) -> str:
        """生成新闻内容"""
        content_parts = []
        
        for category, items in categorized_items.items():
            if not items:
                continue
            
            category_names = {'tech': '科技', 'finance': '财经', 'entertainment': '娱乐'}
            category_name = category_names.get(category, category)
            
            # 分类标题
            if is_main:
                content_parts.append(f"""
                    <div class="category-section">
                        <h2 class="category-title">
                            {category_name}新闻
                            <span style="font-size: 14px; color: #6c757d; font-weight: normal;">
                                ({len(items)}条)
                            </span>
                        </h2>
                """)
            else:
                content_parts.append(f"""
                    <div class="category-section">
                        <h2 class="category-title">
                            {category_name}新闻
                        </h2>
                """)
            
            # 新闻列表
            for item in items[:20]:  # 每个分类最多显示20条
                title = item.get('title', '无标题')
                link = item.get('link', '#')
                description = item.get('description', '')
                source = item.get('source', '未知来源')
                published_at = item.get('published_at', '')
                
                # 截断描述
                if description and len(description) > 150:
                    description = description[:150] + "..."
                
                content_parts.append(f"""
                    <div class="news-item">
                        <div class="news-title">
                            <a href="{link}" target="_blank">{title}</a>
                        </div>
                        <div class="news-meta">
                            <span class="news-source">{source}</span>
                            <span class="news-time">{self._format_time(published_at) if published_at else ''}</span>
                        </div>
                        <div class="news-description">{description}</div>
                    </div>
                """)
            
            content_parts.append('</div>')
        
        if not content_parts:
            return '<div class="category-section"><p style="text-align: center; color: #6c757d;">暂无新闻数据</p></div>'
        
        return ''.join(content_parts)
    
    def _generate_rss_links(self, rss_files: Dict[str, str], current_category: str = None) -> str:
        """生成RSS链接"""
        if not rss_files:
            return ""
        
        rss_items = []
        
        for category, filepath in rss_files.items():
            if category == 'all':
                continue
            
            category_names = {'tech': '科技', 'finance': '财经', 'entertainment': '娱乐'}
            category_name = category_names.get(category, category)
            
            # 相对路径
            rel_path = f"../rss/{category}.xml"
            
            rss_items.append(f"""
                <a href="{rel_path}" target="_blank" title="订阅{category_name}RSS">
                    📡 {category_name}RSS
                </a>
            """)
        
        if not rss_items:
            return ""
        
        return f'<div class="nav">{" ".join(rss_items)}</div>'
    
    def generate_feeds_page(self, rss_files: Dict[str, str], output_dir: str = "docs") -> str:
        """生成RSS订阅页面"""
        if not rss_files:
            return ""
        
        category_names = {'tech': '科技', 'finance': '财经', 'entertainment': '娱乐', 'all': '全部'}
        
        feeds_html = ""
        for category, filepath in rss_files.items():
            rel_path = f"../rss/{category}.xml"
            feeds_html += f"""
                <div class="news-item">
                    <div class="news-title">
                        <a href="{rel_path}" target="_blank">
                            📡 {category_names.get(category, category)} RSS 订阅源
                        </a>
                    </div>
                    <div class="news-description">
                        订阅 {category_names.get(category, category)} 分类的新闻。
                        使用 RSS 阅读器（如 Feedly、Inoreader）添加此链接即可自动接收更新。
                    </div>
                </div>
            """
        
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RSS订阅 - 新闻聚合器</title>
    <style>{self._get_css_styles()}</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📡 RSS订阅</h1>
            <p>使用 RSS 阅读器订阅新闻更新</p>
        </div>
        
        <div class="nav">
            <a href="../index.html">🏠 首页</a>
            <a href="tech.html">📊 科技</a>
            <a href="finance.html">📊 财经</a>
            <a href="entertainment.html">📊 娱乐</a>
        </div>
        
        <div class="category-section">
            <h2 class="category-title">订阅源列表</h2>
            {feeds_html}
        </div>
        
        <div class="category-section">
            <h2 class="category-title">如何使用 RSS</h2>
            <div class="news-item">
                <div class="news-description">
                    <strong>步骤：</strong><br>
                    1. 选择一个 RSS 阅读器（如 Feedly、Inoreader、NewsBlur）<br>
                    2. 点击上方的订阅链接<br>
                    3. 将链接粘贴到阅读器中<br>
                    4. 即可自动接收新闻更新
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>Powered by Auto News Aggregator | 
            <a href="https://github.com/your-username/news-aggregator" target="_blank">GitHub</a></p>
        </div>
    </div>
</body>
</html>"""
        
        # 保存文件
        output_path = Path(output_dir) / "rss"
        output_path.mkdir(parents=True, exist_ok=True)
        
        filepath = output_path / "index.html"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        self.logger.info(f"RSS订阅页面已生成: {filepath}")
        return str(filepath)