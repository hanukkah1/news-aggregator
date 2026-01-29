"""新闻抓取器模块"""
import asyncio
import aiohttp
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json
import time

from .config import Config


class NewsFetcher:
    """新闻抓取器类"""
    
    def __init__(self, config: Config):
        self.config = config
        self.fetcher_config = config.get_fetcher_config()
        self.logger = self._setup_logger()
        self.session = None
        
    def _setup_logger(self) -> logging.Logger:
        """设置日志"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        # 如果没有handler，添加一个
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    async def _create_session(self):
        """创建HTTP会话"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=self.fetcher_config.get('timeout', 30))
            headers = {
                'User-Agent': self.fetcher_config.get('user_agent', 'Mozilla/5.0')
            }
            self.session = aiohttp.ClientSession(timeout=timeout, headers=headers)
    
    async def close_session(self):
        """关闭HTTP会话"""
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None
    
    async def fetch_url(self, url: str, retry_count: int = 0) -> Optional[str]:
        """获取URL内容"""
        max_retries = self.fetcher_config.get('retry_times', 3)
        
        try:
            await self._create_session()
            
            async with self.session.get(url) as response:
                if response.status == 200:
                    content = await response.text('utf-8')
                    self.logger.info(f"成功获取URL: {url}")
                    return content
                else:
                    self.logger.warning(f"获取URL失败: {url} (状态码: {response.status})")
                    
        except Exception as e:
            self.logger.error(f"获取URL异常: {url} - {e}")
        
        # 重试逻辑
        if retry_count < max_retries:
            delay = 2 ** retry_count  # 指数退避
            self.logger.info(f"{url} 重试 {retry_count + 1}/{max_retries}，等待 {delay}秒...")
            await asyncio.sleep(delay)
            return await self.fetch_url(url, retry_count + 1)
        
        return None
    
    async def fetch_source(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """抓取单个新闻源"""
        name = source.get('name', 'Unknown')
        url = source.get('url')
        
        if not url:
            self.logger.warning(f"新闻源 '{name}' 没有配置URL")
            return None
        
        self.logger.info(f"开始抓取: {name} ({url})")
        
        content = await self.fetch_url(url)
        if not content:
            self.logger.error(f"抓取失败: {name}")
            return None
        
        # 延迟请求，避免过于频繁
        delay = self.fetcher_config.get('delay_between_requests', 2)
        await asyncio.sleep(delay)
        
        return {
            'name': name,
            'url': url,
            'content': content,
            'fetched_at': datetime.now().isoformat(),
            'category': source.get('category', 'unknown')
        }
    
    async def fetch_category(self, category: str) -> List[Dict[str, Any]]:
        """抓取指定分类的所有新闻源"""
        sources = self.config.get_enabled_sources(category)
        
        if not sources:
            self.logger.warning(f"分类 '{category}' 没有启用的新闻源")
            return []
        
        self.logger.info(f"开始抓取分类 '{category}'，共 {len(sources)} 个源")
        
        # 为每个源添加分类信息
        for source in sources:
            source['category'] = category
        
        # 并发抓取
        tasks = [self.fetch_source(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤失败的结果
        successful_results = []
        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"抓取异常: {result}")
            elif result is not None:
                successful_results.append(result)
        
        self.logger.info(f"分类 '{category}' 抓取完成: {len(successful_results)}/{len(sources)} 成功")
        
        return successful_results
    
    async def fetch_all_categories(self) -> Dict[str, List[Dict[str, Any]]]:
        """抓取所有分类的新闻"""
        categories = self.config.get_categories()
        results = {}
        
        for category in categories:
            results[category] = await self.fetch_category(category)
        
        return results
    
    async def fetch_all(self) -> Dict[str, Any]:
        """执行完整的抓取流程"""
        self.logger.info("开始执行新闻抓取任务")
        
        start_time = time.time()
        
        try:
            # 抓取所有分类
            category_results = await self.fetch_all_categories()
            
            # 统计信息
            total_sources = sum(len(sources) for sources in category_results.values())
            successful_sources = sum(
                len(sources) for sources in category_results.values()
            )
            
            elapsed_time = time.time() - start_time
            
            result = {
                'timestamp': datetime.now().isoformat(),
                'categories': category_results,
                'stats': {
                    'total_categories': len(category_results),
                    'total_sources': total_sources,
                    'successful_sources': successful_sources,
                    'elapsed_time': round(elapsed_time, 2)
                }
            }
            
            self.logger.info(f"抓取任务完成，耗时 {elapsed_time:.2f} 秒")
            
            return result
            
        except Exception as e:
            self.logger.error(f"抓取任务异常: {e}")
            raise
        finally:
            await self.close_session()
    
    def save_results(self, results: Dict[str, Any], output_dir: str = "data"):
        """保存抓取结果到文件"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"news_data_{timestamp}.json"
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"抓取结果已保存到: {filepath}")
        
        # 保存最新数据的软链接
        latest_path = Path(output_dir) / "latest.json"
        if latest_path.exists():
            latest_path.unlink()
        
        try:
            latest_path.symlink_to(filename)
            self.logger.info(f"已创建最新数据链接: {latest_path}")
        except:
            # Windows 不支持符号链接，复制文件
            import shutil
            shutil.copy2(filepath, latest_path)
            self.logger.info(f"已复制最新数据到: {latest_path}")
    
    async def run(self, save: bool = True, output_dir: str = "data") -> Dict[str, Any]:
        """运行抓取任务"""
        results = await self.fetch_all()
        
        if save:
            self.save_results(results, output_dir)
        
        return results