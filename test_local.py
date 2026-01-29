#!/usr/bin/env python3
"""本地测试脚本"""
import asyncio
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from config import Config
from fetcher import NewsFetcher
from parser import NewsParser
from rss_generator import RSSGenerator
from html_generator import HTMLGenerator


async def test_local():
    """本地测试函数"""
    print("=" * 60)
    print("新闻聚合器本地测试")
    print("=" * 60)
    
    try:
        # 1. 测试配置加载
        print("\n1. 测试配置加载...")
        config = Config("config.yaml")
        print(f"   ✓ 配置加载成功")
        print(f"   ✓ 分类: {config.get_categories()}")
        
        # 2. 测试新闻抓取（单个分类）
        print("\n2. 测试新闻抓取...")
        fetcher = NewsFetcher(config)
        
        # 只测试科技分类
        tech_results = await fetcher.fetch_category('tech')
        print(f"   ✓ 科技分类抓取成功: {len(tech_results)} 个源")
        
        # 3. 测试新闻解析
        print("\n3. 测试新闻解析...")
        parser = NewsParser()
        sources_config = config.get_enabled_sources('tech')
        items = parser.parse_all(tech_results, sources_config)
        print(f"   ✓ 新闻解析成功: {len(items)} 条新闻")
        
        # 4. 测试RSS生成
        print("\n4. 测试RSS生成...")
        rss_generator = RSSGenerator(config)
        categorized_items = {'tech': items[:10]}  # 只取前10条测试
        rss_files = rss_generator.generate_all_rss(categorized_items, "test_output/rss")
        print(f"   ✓ RSS生成成功: {len(rss_files)} 个文件")
        
        # 5. 测试HTML生成
        print("\n5. 测试HTML生成...")
        html_generator = HTMLGenerator(config)
        main_page = html_generator.generate_main_page(
            categorized_items, 
            rss_files, 
            "test_output/docs"
        )
        print(f"   ✓ HTML生成成功: {main_page}")
        
        # 6. 显示测试结果
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
        print(f"生成的文件在: test_output/")
        print(f"新闻数量: {len(items)}")
        print(f"RSS文件: {len(rss_files)}")
        print(f"HTML页面: 1")
        print("=" * 60)
        
        # 清理测试文件
        import shutil
        if Path("test_output").exists():
            shutil.rmtree("test_output")
            print("测试文件已清理")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("错误: 需要Python 3.9或更高版本")
        sys.exit(1)
    
    # 运行测试
    success = asyncio.run(test_local())
    sys.exit(0 if success else 1)