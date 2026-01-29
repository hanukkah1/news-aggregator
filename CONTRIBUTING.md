# 贡献指南

感谢您对新闻聚合器项目的兴趣！我们欢迎所有形式的贡献，包括代码、文档、bug 报告和功能建议。

## 如何贡献

### 1. 报告 Bug

如果您发现了 bug，请：
1. 检查 [Issues](https://github.com/your-username/news-aggregator/issues) 是否已被报告
2. 如果没有，创建一个新的 Issue
3. 提供详细的复现步骤和环境信息

### 2. 请求新功能

如果您有新功能的想法：
1. 检查 [Issues](https://github.com/your-username/news-aggregator/issues) 是否已被提出
2. 创建一个新的 Feature Request Issue
3. 描述功能的使用场景和预期行为

### 3. 贡献代码

#### 准备工作

1. Fork 本仓库
2. 克隆到本地：
   ```bash
   git clone https://github.com/your-username/news-aggregator.git
   cd news-aggregator
   ```
3. 安装开发依赖：
   ```bash
   pip install -r requirements-dev.txt
   ```
4. 安装 pre-commit hooks：
   ```bash
   pre-commit install
   ```

#### 开发流程

1. 创建特性分支：
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. 编写代码和测试：
   ```bash
   # 运行测试
   python -m pytest tests/
   
   # 代码格式化
   black src/
   
   # 代码检查
   flake8 src/
   ```

3. 提交更改：
   ```bash
   git add .
   git commit -m "feat: 添加新功能"
   git push origin feature/amazing-feature
   ```

4. 创建 Pull Request：
   - 描述变更内容
   - 关联相关 Issue
   - 确保所有检查通过

#### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

示例：
```
feat: 添加 Telegram 通知支持
fix: 修复 RSS 生成时的编码问题
docs: 更新部署指南
```

### 4. 添加新闻源

#### 添加新的新闻源配置

编辑 `config.yaml`：

```yaml
news_sources:
  tech:
    - name: "新网站名称"
      url: "https://example.com/news"
      selector: ".news-item"  # 新闻项的 CSS 选择器
      link_selector: "a"      # 链接的选择器
      title_selector: ".title" # 标题的选择器
      desc_selector: ".desc"   # 描述的选择器
      enabled: true
```

#### 测试新闻源

1. 本地测试：
   ```bash
   python test_local.py
   ```

2. 或者创建测试脚本：
   ```python
   # test_new_source.py
   import asyncio
   from src.fetcher import NewsFetcher
   from src.config import Config
   
   async def test():
       config = Config()
       fetcher = NewsFetcher(config)
       result = await fetcher.fetch_category('tech')
       print(f"抓取到 {len(result)} 个源")
   
   asyncio.run(test())
   ```

### 5. 改进文档

文档的改进同样重要！您可以：
- 修正错别字
- 补充缺失的说明
- 翻译文档
- 添加示例

## 代码规范

### Python 代码

- 遵循 PEP 8 规范
- 使用类型注解
- 函数和类要有文档字符串
- 代码行长度不超过 88 字符（Black 默认）

### 项目结构

```
news-aggregator/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── config.py          # 配置管理
│   ├── fetcher.py         # 新闻抓取
│   ├── parser.py          # 新闻解析
│   ├── rss_generator.py   # RSS 生成
│   ├── html_generator.py  # HTML 生成
│   ├── utils.py           # 工具函数
│   └── main.py            # 主程序
├── tests/                 # 测试代码
├── docs/                  # 文档
├── data/                  # 数据
├── logs/                  # 日志
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖
└── README.md             # 项目说明
```

### 测试

- 新功能需要包含测试
- 测试文件放在 `tests/` 目录
- 使用 pytest 框架
- 测试覆盖率目标：80%+

```bash
# 运行测试
python -m pytest tests/ -v

# 查看覆盖率
python -m pytest tests/ --cov=src --cov-report=html
```

## 代码审查流程

1. **自动检查**：
   - GitHub Actions 自动运行测试
   - 代码格式化检查
   - 类型检查

2. **人工审查**：
   - 至少需要一位维护者批准
   - 审查重点：
     - 代码正确性
     - 性能影响
     - 向后兼容性
     - 文档更新

3. **合并**：
   - 使用 Squash and Merge
   - 保持提交历史整洁

## 行为准则

我们采用 [Contributor Covenant](https://www.contributor-covenant.org/) 行为准则：

- 使用友好和包容的语言
- 尊重不同的观点和经历
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同理心

## 问题和讨论

- **技术问题**：在 GitHub Discussions 中提问
- **功能建议**：创建 Feature Request Issue
- **一般讨论**：使用 GitHub Discussions

## 赞助

如果您觉得这个项目有帮助，可以考虑：
- ⭐ 给项目加星
- 🤝 贡献代码
- 💰 [赞助](https://github.com/sponsors/your-username)

## 感谢

感谢所有贡献者的付出！🎉

<a href="https://github.com/your-username/news-aggregator/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=your-username/news-aggregator" />
</a>