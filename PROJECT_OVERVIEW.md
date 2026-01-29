# 新闻聚合器项目总览

## 🎯 项目简介

这是一个基于 GitHub Actions 的自动化新闻聚合和 RSS 订阅源生成器。它每天早中晚定时获取最新的科技、财经和娱乐新闻，自动生成 RSS 订阅源和美观的网页展示。

## ✨ 核心功能

### 📰 新闻聚合
- **多分类支持**：科技、财经、娱乐三大分类
- **自动抓取**：每天早中晚定时运行（可配置）
- **智能解析**：基于 CSS 选择器的新闻解析
- **数据去重**：自动去除重复新闻
- **时间过滤**：只保留最新新闻

### 🌐 RSS 订阅
- **标准格式**：生成标准 RSS 2.0 订阅源
- **多分类 RSS**：每个分类独立 RSS
- **总 RSS**：所有新闻汇总的 RSS
- **自动更新**：随抓取任务自动更新

### 📊 网页展示
- **响应式设计**：适配桌面和移动端
- **多主题支持**：modern、dark、minimal 三种主题
- **分类页面**：每个分类独立页面
- **统计信息**：显示新闻数量和更新时间

### ⚡ 自动化
- **GitHub Actions**：无需服务器，完全自动化
- **定时调度**：每天固定时间自动运行
- **自动部署**：自动部署到 GitHub Pages
- **数据清理**：自动清理旧数据

## 🏗️ 技术架构

### 核心组件

```
┌─────────────────────────────────────────┐
│           GitHub Actions                │
│      (定时调度 / 手动触发)               │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         Python 主程序 (src/)             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │ Config  │  │ Fetcher │  │ Parser  │  │
│  └─────────┘  └─────────┘  └─────────┘  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  RSS    │  │  HTML   │  │ Utils   │  │
│  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│           输出文件                        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  docs/  │  │  rss/   │  │  data/  │  │
│  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         GitHub Pages (Web)               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  主页   │  │ 分类页  │  │ RSS页   │  │
│  └─────────┘  └─────────┘  └─────────┘  │
└─────────────────────────────────────────┘
```

### 技术栈

- **Python 3.9+**：核心编程语言
- **aiohttp**：异步 HTTP 请求
- **BeautifulSoup4**：HTML 解析
- **Feedgen**：RSS 生成
- **Jinja2**：HTML 模板（可选）
- **PyYAML**：配置文件解析
- **GitHub Actions**：自动化调度
- **GitHub Pages**：静态页面托管

## 📁 项目结构

```
news-aggregator/
├── src/                    # 源代码
│   ├── config.py          # 配置管理
│   ├── fetcher.py         # 新闻抓取
│   ├── parser.py          # 新闻解析
│   ├── rss_generator.py   # RSS 生成
│   ├── html_generator.py  # HTML 生成
│   ├── utils.py           # 工具函数
│   └── main.py            # 主程序
├── .github/workflows/     # GitHub Actions
│   └── news-aggregator.yml
├── config.yaml            # 配置文件
├── requirements.txt       # 依赖
├── run.py                 # 启动脚本
├── test_local.py          # 本地测试
├── README.md              # 项目说明
├── QUICKSTART.md          # 快速开始
├── DEPLOYMENT.md          # 部署指南
├── CONTRIBUTING.md        # 贡献指南
├── PROJECT_STRUCTURE.md   # 结构说明
└── PROJECT_OVERVIEW.md    # 本文件
```

## 🔄 工作流程

### 1. 配置阶段
```
config.yaml → Config → 验证配置 → 创建目录
```

### 2. 抓取阶段
```
新闻源URL → NewsFetcher → 异步HTTP请求 → 原始HTML
```

### 3. 解析阶段
```
原始HTML → NewsParser → CSS选择器 → 结构化数据
```

### 4. 生成阶段
```
结构化数据 → RSSGenerator → RSS 2.0 → .xml文件
结构化数据 → HTMLGenerator → 响应式HTML → .html文件
```

### 5. 部署阶段
```
docs/ + rss/ → GitHub Pages → 静态网站
```

## 🎨 输出示例

### RSS 订阅源
```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>新闻聚合器 - 科技分类</title>
    <description>自动聚合的科技新闻</description>
    <item>
      <title>最新科技新闻标题</title>
      <link>https://example.com/news</link>
      <description>新闻摘要...</description>
      <pubDate>Mon, 29 Jan 2024 12:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
```

### HTML 页面
```html
<!DOCTYPE html>
<html>
<head>
  <title>新闻聚合器 - 首页</title>
  <style>/* 现代化主题样式 */</style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>📰 新闻聚合器</h1>
    </div>
    <div class="nav">
      <a href="category/tech.html">科技</a>
      <a href="category/finance.html">财经</a>
      <a href="category/entertainment.html">娱乐</a>
    </div>
    <div class="stats">
      <!-- 统计信息 -->
    </div>
    <!-- 新闻列表 -->
  </div>
</body>
</html>
```

## 🔧 配置示例

### 新闻源配置
```yaml
news_sources:
  tech:
    - name: "36氪"
      url: "https://36kr.com"
      selector: ".article-item"
      link_selector: "a"
      title_selector: ".article-title"
      desc_selector: ".article-desc"
      enabled: true
```

### 调度配置
```yaml
schedule:
  - cron: '0 0,4,10 * * *'  # UTC时间：0:00, 4:00, 10:00
```

### 主题配置
```yaml
html:
  theme: "modern"  # modern, dark, minimal
```

## 📊 统计信息

每次运行后会生成统计信息：

```json
{
  "timestamp": "2024-01-29T12:00:00",
  "categories": {
    "tech": 15,
    "finance": 12,
    "entertainment": 10
  },
  "total_items": 37,
  "rss_files": 4,
  "html_pages": 4
}
```

## 🚀 部署方式

### 方式一：GitHub Actions（推荐）
- ✅ 无需服务器
- ✅ 完全自动化
- ✅ 免费使用
- ✅ 易于维护

### 方式二：本地运行
- ✅ 适合开发测试
- ✅ 完全控制
- ✅ 需要本地环境

### 方式三：自建服务器
- ✅ 完全自定义
- ✅ 需要服务器
- ✅ 需要维护

## 🎯 使用场景

### 个人使用
- 每日新闻聚合
- RSS 订阅管理
- 个人新闻主页

### 团队使用
- 团队新闻共享
- 行业资讯聚合
- 竞品监控

### 企业使用
- 行业动态追踪
- 竞争情报收集
- 内部知识库

## 📈 扩展性

### 支持扩展
- ✅ 新闻源（无限）
- ✅ 分类（无限）
- ✅ 输出格式（RSS, HTML, JSON, XML...）
- ✅ 通知方式（Telegram, Slack, Email...）
- ✅ 存储后端（本地, S3, 数据库...）

### 未来计划
- [ ] 支持更多新闻源解析规则
- [ ] 添加机器学习去重
- [ ] 支持新闻摘要生成
- [ ] 添加搜索功能
- [ ] 支持多语言

## 🤝 社区

### 贡献方式
- 🐛 报告 Bug
- 💡 功能建议
- 📝 文档改进
- 💻 代码贡献
- 📰 添加新闻源

### 交流渠道
- GitHub Issues：问题反馈
- GitHub Discussions：技术讨论
- Pull Requests：代码贡献

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- GitHub Actions 提供自动化支持
- 各新闻源提供公开内容
- 开源社区的优秀工具库

## 📞 支持

如有问题，请在 GitHub Issues 中提出：
https://github.com/your-username/news-aggregator/issues

---

**开始使用**：查看 [QUICKSTART.md](QUICKSTART.md) 快速上手！