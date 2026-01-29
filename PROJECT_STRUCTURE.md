# 项目结构说明

## 目录结构

```
news-aggregator/
├── .github/                    # GitHub 配置
│   ├── workflows/              # GitHub Actions 工作流
│   │   └── news-aggregator.yml
│   ├── ISSUE_TEMPLATE/         # Issue 模板
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md # PR 模板
│
├── src/                        # 源代码
│   ├── __init__.py            # 包初始化
│   ├── config.py              # 配置管理
│   ├── fetcher.py             # 新闻抓取器
│   ├── parser.py              # 新闻解析器
│   ├── rss_generator.py       # RSS 生成器
│   ├── html_generator.py      # HTML 生成器
│   ├── utils.py               # 工具函数
│   └── main.py                # 主程序入口
│
├── templates/                  # HTML 模板（可选）
│   ├── index.html
│   └── category.html
│
├── data/                       # 数据目录（自动生成）
│   ├── .gitkeep
│   ├── news_data_*.json       # 新闻数据
│   ├── latest.json            # 最新数据链接
│   └── stats.json             # 统计信息
│
├── docs/                       # HTML 输出（自动生成）
│   ├── index.html             # 主页面
│   ├── category/
│   │   ├── tech.html          # 科技分类页面
│   │   ├── finance.html       # 财经分类页面
│   │   └── entertainment.html # 娱乐分类页面
│   └── rss/
│       └── index.html         # RSS 订阅页面
│
├── rss/                        # RSS 输出（自动生成）
│   ├── tech.xml               # 科技 RSS
│   ├── finance.xml            # 财经 RSS
│   ├── entertainment.xml      # 娱乐 RSS
│   └── all.xml                # 总 RSS
│
├── logs/                       # 日志目录（自动生成）
│   └── news-aggregator.log    # 运行日志
│
├── tests/                      # 测试代码（可选）
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_fetcher.py
│   ├── test_parser.py
│   └── test_rss_generator.py
│
├── config.yaml                 # 主配置文件
├── requirements.txt            # 生产依赖
├── requirements-dev.txt        # 开发依赖
├── run.py                      # 启动脚本
├── test_local.py              # 本地测试脚本
├── README.md                   # 项目说明
├── QUICKSTART.md              # 快速开始
├── DEPLOYMENT.md              # 部署指南
├── CONTRIBUTING.md            # 贡献指南
├── PROJECT_STRUCTURE.md       # 本文件
├── LICENSE                     # 许可证
├── .gitignore                  # Git 忽略文件
├── .editorconfig              # 编辑器配置
├── .pre-commit-config.yaml    # Pre-commit 配置
└── setup.py                   # 包安装配置（可选）
```

## 核心模块说明

### 1. 配置管理 (`config.py`)

**功能**：
- 加载和验证 YAML 配置文件
- 提供统一的配置访问接口
- 管理输出目录结构

**主要类**：
```python
class Config:
    def __init__(self, config_path: str = "config.yaml")
    def get_schedule(self) -> List[str]
    def get_news_sources(self, category: str = None) -> Dict[str, List[Dict]]
    def get_enabled_sources(self, category: str) -> List[Dict]
    def validate(self) -> bool
    def create_directories(self)
```

### 2. 新闻抓取器 (`fetcher.py`)

**功能**：
- 异步 HTTP 请求
- 并发抓取多个新闻源
- 错误重试机制
- 数据保存

**主要类**：
```python
class NewsFetcher:
    async def fetch_url(self, url: str) -> Optional[str]
    async def fetch_source(self, source: Dict) -> Optional[Dict]
    async def fetch_category(self, category: str) -> List[Dict]
    async def fetch_all(self) -> Dict[str, Any]
    def save_results(self, results: Dict[str, Any], output_dir: str)
```

### 3. 新闻解析器 (`parser.py`)

**功能**：
- HTML 解析（使用 BeautifulSoup）
- CSS 选择器提取
- 数据清洗和格式化
- 去重和过滤

**主要类**：
```python
class NewsParser:
    def parse_source(self, source_data: Dict, source_config: Dict) -> List[Dict]
    def parse_all(self, sources_data: List[Dict], sources_config: List[Dict]) -> List[Dict]
    def deduplicate_items(self, items: List[Dict]) -> List[Dict]
    def filter_by_time(self, items: List[Dict], hours: int = 24) -> List[Dict]
```

### 4. RSS 生成器 (`rss_generator.py`)

**功能**：
- 生成标准 RSS 2.0 格式
- 支持多分类 RSS
- 支持总 RSS 汇总

**主要类**：
```python
class RSSGenerator:
    def create_feed(self, category: str, items: List[Dict]) -> FeedGenerator
    def generate_category_rss(self, category: str, items: List[Dict]) -> str
    def generate_all_rss(self, categorized_items: Dict[str, List[Dict]]) -> Dict[str, str]
    def generate_index_rss(self, all_items: List[Dict]) -> str
```

### 5. HTML 生成器 (`html_generator.py`)

**功能**：
- 生成响应式 HTML 页面
- 支持多主题（modern, dark, minimal）
- 生成分类页面和主页面
- 统计信息展示

**主要类**：
```python
class HTMLGenerator:
    def generate_main_page(self, categorized_items: Dict, rss_files: Dict) -> str
    def generate_category_pages(self, categorized_items: Dict, rss_files: Dict) -> Dict[str, str]
    def generate_feeds_page(self, rss_files: Dict) -> str
```

### 6. 主程序 (`main.py`)

**功能**：
- 协调各个模块
- 执行完整流程
- 错误处理和日志记录

**主要函数**：
```python
async def run_news_aggregator(config_path: str = "config.yaml") -> bool
async def main()
```

## 数据流

```
config.yaml
    ↓
Config (配置加载)
    ↓
NewsFetcher (抓取新闻)
    ↓
Raw HTML Data
    ↓
NewsParser (解析数据)
    ↓
Structured News Items
    ↓
RSSGenerator (生成 RSS)
    ↓
HTMLGenerator (生成 HTML)
    ↓
Output Files (docs/, rss/, data/)
```

## GitHub Actions 工作流

### 触发方式

1. **定时触发**：每天 8:00, 12:00, 18:00 (UTC)
2. **手动触发**：通过 GitHub Actions 界面
3. **代码推送**：修改配置或代码时

### 执行步骤

1. **检出代码**：checkout 仓库
2. **安装依赖**：pip install -r requirements.txt
3. **运行程序**：python src/main.py
4. **部署到 GitHub Pages**：上传 docs/ 和 rss/ 目录
5. **清理旧数据**：删除 30 天前的数据

## 配置文件说明

### config.yaml

```yaml
# 调度设置
schedule:
  - cron: '0 0,4,10 * * *'

# 新闻源配置
news_sources:
  tech:
    - name: "网站名称"
      url: "https://example.com"
      selector: ".news-item"
      link_selector: "a"
      title_selector: ".title"
      desc_selector: ".desc"
      enabled: true

# RSS 配置
rss:
  output_dir: "rss"
  max_items_per_feed: 50
  ttl: 180

# HTML 配置
html:
  output_dir: "docs"
  max_items_per_page: 20
  theme: "modern"

# 存储配置
storage:
  data_dir: "data"
  keep_days: 30
  deduplicate: true

# 抓取配置
fetcher:
  timeout: 30
  retry_times: 3
  user_agent: "Mozilla/5.0..."
  delay_between_requests: 2

# 通知配置（可选）
notifications:
  telegram:
    enabled: false
    bot_token: ""
    chat_id: ""

# 日志配置
logging:
  level: "INFO"
  file: "logs/news-aggregator.log"
```

## 扩展开发

### 添加新的新闻源

1. 在 `config.yaml` 中添加配置
2. 测试抓取和解析
3. 提交代码

### 添加新的输出格式

1. 在 `src/` 目录创建新的生成器
2. 在 `main.py` 中集成
3. 更新配置文件

### 添加新的通知方式

1. 在 `config.yaml` 中添加配置
2. 在 `src/` 目录创建通知模块
3. 在 `main.py` 中集成

## 性能优化

### 抓取优化
- 使用异步请求（aiohttp）
- 并发抓取多个源
- 指数退避重试

### 存储优化
- 数据去重
- 定期清理旧数据
- 使用软链接引用最新数据

### 生成优化
- 按需生成页面
- 缓存中间结果
- 增量更新

## 安全考虑

### 数据安全
- 不存储敏感信息
- 定期清理旧数据
- 使用 GitHub Secrets 管理密钥

### 网络安全
- 使用 HTTPS
- 验证 SSL 证书
- 限制请求频率

### 代码安全
- 依赖包扫描
- 代码审查
- 自动化测试