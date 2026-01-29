# 自动化新闻聚合器 (Auto News Aggregator)

一个基于 GitHub Actions 的自动化新闻聚合和 RSS 订阅源生成器，每天早中晚定时获取最新的科技、财经和娱乐新闻。

## ✨ 功能特性

- 🔄 **自动化采集**：每天早中晚定时获取最新新闻
- 📰 **多分类支持**：科技、财经、娱乐三大分类
- 🌐 **RSS 生成**：自动生成标准化 RSS 订阅源
- 📊 **网页展示**：美观的新闻汇总页面
- ⚡ **GitHub Actions**：无需服务器，完全自动化运行
- 🎯 **可配置**：灵活的源配置和调度设置

## 🚀 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮将本仓库复制到您的 GitHub 账户。

### 2. 启用 GitHub Pages

进入仓库设置：
- Settings → Pages → Source → Deploy from a branch
- 选择 `gh-pages` 分支和 `/ (root)` 目录
- 点击 Save

### 3. 配置（可选）

编辑 `config.yaml` 文件自定义：
- 新闻源 URL
- 抓取频率
- RSS 生成设置
- 网页展示样式

### 4. 手动触发（可选）

进入 Actions 标签页，选择 "News Aggregator" workflow，点击 "Run workflow" 手动触发。

## 📁 项目结构

```
news-aggregator/
├── .github/
│   └── workflows/
│       └── news-aggregator.yml    # GitHub Actions 工作流
├── src/
│   ├── __init__.py
│   ├── config.py                  # 配置管理
│   ├── fetcher.py                 # 新闻抓取器
│   ├── parser.py                  # 新闻解析器
│   ├── rss_generator.py           # RSS 生成器
│   ├── html_generator.py          # HTML 页面生成器
│   └── main.py                    # 主程序入口
├── templates/
│   ├── index.html                 # 主页面模板
│   └── category.html              # 分类页面模板
├── data/
│   └── .gitkeep                   # 数据目录占位符
├── config.yaml                    # 配置文件
├── requirements.txt               # Python 依赖
├── .gitignore
└── README.md
```

## 📖 使用指南

### 配置新闻源

编辑 `config.yaml` 文件添加或修改新闻源：

```yaml
news_sources:
  tech:
    - name: "科技日报"
      url: "https://example.com/tech"
      selector: ".news-item"
    
  finance:
    - name: "财经新闻"
      url: "https://example.com/finance"
      selector: ".article"
    
  entertainment:
    - name: "娱乐资讯"
      url: "https://example.com/entertainment"
      selector: ".news"
```

### 调度设置

在 `.github/workflows/news-aggregator.yml` 中配置：

```yaml
schedule:
  # 每天 8:00, 12:00, 18:00 运行
  - cron: '0 8,12,18 * * *'
```

## 🔧 技术栈

- **Python 3.9+**：核心编程语言
- **Requests**：HTTP 请求库
- **BeautifulSoup4**：HTML 解析
- **Feedgen**：RSS 生成
- **Jinja2**：HTML 模板引擎
- **GitHub Actions**：自动化调度
- **GitHub Pages**：静态页面托管

## 📊 输出示例

### RSS 订阅源
- `https://yourusername.github.io/news-aggregator/rss/tech.xml`
- `https://yourusername.github.io/news-aggregator/rss/finance.xml`
- `https://yourusername.github.io/news-aggregator/rss/entertainment.xml`

### 网页展示
- 主页面：`https://yourusername.github.io/news-aggregator/`
- 分类页面：`https://yourusername.github.io/news-aggregator/category/tech.html`

## ⚙️ 高级配置

### 自定义抓取规则

支持多种解析方式：
- CSS 选择器
- XPath
- 正则表达式

### 数据存储

- 新闻数据存储在 `data/` 目录
- 支持历史记录和去重
- 可配置保留天数

### 通知集成

可选集成：
- Telegram Bot
- Slack Webhook
- Email 通知

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🙏 致谢

- GitHub Actions 提供自动化支持
- 各新闻源提供公开内容
- 开源社区的优秀工具库

## 📞 支持

如有问题，请在 GitHub Issues 中提出。