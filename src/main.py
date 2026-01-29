"""新闻聚合器主程序"""
import asyncio
import logging
from pathlib import Path
import sys
import os

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from config import Config
from fetcher import NewsFetcher
from parser import NewsParser
from rss_generator import RSSGenerator
from html_generator import HTMLGenerator


def setup_logging(config: Config):
    """设置日志"""
    log_config = config.get_logging_config()
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    
    # 创建日志目录
    log_file = log_config.get('file', 'logs/news-aggregator.log')
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 配置日志
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


async def run_news_aggregator(config_path: str = "config.yaml"):
    """运行新闻聚合器"""
    try:
        # 加载配置
        print("正在加载配置...")
        config = Config(config_path)
        
        # 验证配置
        if not config.validate():
            print("配置验证失败，请检查配置文件")
            return False
        
        # 设置日志
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        logger.info("新闻聚合器启动")
        
        # 创建输出目录
        config.create_directories()
        
        # 步骤1: 抓取新闻
        print("正在抓取新闻...")
        logger.info("开始抓取新闻")
        
        fetcher = NewsFetcher(config)
        results = await fetcher.run(save=True)
        
        print(f"抓取完成: {results['stats']['successful_sources']}/{results['stats']['total_sources']} 个源成功")
        logger.info(f"抓取完成: {results['stats']['successful_sources']}/{results['stats']['total_sources']} 个源成功")
        
        # 步骤2: 解析新闻
        print("正在解析新闻...")
        logger.info("开始解析新闻")
        
        parser = NewsParser()
        categorized_items = parser.parse_category_data(results['categories'], config)
        
        # 去重和过滤
        for category in categorized_items:
            items = categorized_items[category]
            items = parser.deduplicate_items(items)
            items = parser.filter_by_time(items, hours=24)  # 只保留24小时内的新闻
            items = parser.sort_items(items)
            categorized_items[category] = items
        
        print(f"解析完成: {sum(len(items) for items in categorized_items.values())} 条新闻")
        logger.info(f"解析完成: {sum(len(items) for items in categorized_items.values())} 条新闻")
        
        # 步骤3: 生成RSS
        print("正在生成RSS订阅源...")
        logger.info("开始生成RSS订阅源")
        
        rss_generator = RSSGenerator(config)
        output_dirs = config.get_output_dirs()
        
        rss_files = rss_generator.generate_all_rss(categorized_items, output_dirs['rss'])
        
        # 生成总RSS
        all_items = []
        for items in categorized_items.values():
            all_items.extend(items)
        all_items = parser.sort_items(all_items)
        
        if all_items:
            rss_generator.generate_index_rss(all_items, output_dirs['rss'])
        
        print(f"RSS生成完成: {len(rss_files)} 个文件")
        logger.info(f"RSS生成完成: {len(rss_files)} 个文件")
        
        # 步骤4: 生成HTML页面
        print("正在生成HTML页面...")
        logger.info("开始生成HTML页面")
        
        html_generator = HTMLGenerator(config)
        
        # 生成主页面
        main_page = html_generator.generate_main_page(
            categorized_items, 
            rss_files, 
            output_dirs['html']
        )
        
        # 生成分类页面
        category_pages = html_generator.generate_category_pages(
            categorized_items, 
            rss_files, 
            output_dirs['html']
        )
        
        # 生成RSS订阅页面
        feeds_page = html_generator.generate_feeds_page(rss_files, output_dirs['html'])
        
        print(f"HTML生成完成: {len(category_pages) + 2} 个页面")
        logger.info(f"HTML生成完成: {len(category_pages) + 2} 个页面")
        
        # 步骤5: 生成统计信息
        stats = {
            'timestamp': results['timestamp'],
            'categories': {},
            'total_items': 0,
            'rss_files': len(rss_files),
            'html_pages': len(category_pages) + 2
        }
        
        for category, items in categorized_items.items():
            stats['categories'][category] = len(items)
            stats['total_items'] += len(items)
        
        # 保存统计信息
        stats_file = Path(output_dirs['data']) / "stats.json"
        import json
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"统计信息已保存: {stats_file}")
        logger.info(f"统计信息已保存: {stats_file}")
        
        # 输出总结
        print("\n" + "="*50)
        print("新闻聚合器运行完成！")
        print("="*50)
        print(f"抓取源: {results['stats']['successful_sources']}/{results['stats']['total_sources']}")
        print(f"新闻总数: {stats['total_items']}")
        print(f"RSS文件: {stats['rss_files']}")
        print(f"HTML页面: {stats['html_pages']}")
        print(f"耗时: {results['stats']['elapsed_time']}秒")
        print(f"输出目录: {output_dirs['html']}")
        print("="*50)
        
        logger.info("新闻聚合器运行完成")
        
        return True
        
    except Exception as e:
        print(f"运行失败: {e}")
        logging.error(f"运行失败: {e}", exc_info=True)
        return False


async def main():
    """主函数"""
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
    else:
        config_path = "config.yaml"
    
    success = await run_news_aggregator(config_path)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())