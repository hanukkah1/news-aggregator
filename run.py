#!/usr/bin/env python3
"""新闻聚合器启动脚本"""
import asyncio
import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from main import main


if __name__ == "__main__":
    # 检查Python版本
    if sys.version_info < (3, 9):
        print("错误: 需要Python 3.9或更高版本")
        sys.exit(1)
    
    # 运行主程序
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"运行错误: {e}")
        sys.exit(1)