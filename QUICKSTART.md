# 快速开始指南

## 5分钟快速部署

### 方式一：GitHub Actions（推荐）

1. **Fork 仓库**
   - 访问：https://github.com/your-username/news-aggregator
   - 点击 "Fork" 按钮

2. **启用 GitHub Pages**
   - 进入 Settings → Pages
   - Source 选择：Deploy from a branch
   - Branch 选择：gh-pages，目录：/(root)
   - 点击 Save

3. **手动触发运行**
   - 进入 Actions 标签页
   - 选择 "News Aggregator"
   - 点击 "Run workflow"
   - 等待 2-5 分钟

4. **查看结果**
   - 主页面：`https://your-username.github.io/news-aggregator/`
   - RSS订阅：`https://your-username.github.io/news-aggregator/rss/tech.xml`

### 方式二：本地运行

1. **安装环境**
   ```bash
   # 克隆仓库
   git clone https://github.com/your-username/news-aggregator.git
   cd news-aggregator
   
   # 安装依赖
   pip install -r requirements.txt
   ```

2. **本地测试**
   ```bash
   # 运行测试脚本
   python test_local.py
   ```

3. **运行主程序**
   ```bash
   # 使用默认配置
   python src/main.py
   ```

4. **查看输出**
   - HTML 页面：`docs/index.html`
   - RSS 文件：`rss/tech.xml`
   - 数据文件：`data/latest.json`

## 配置说明

### 修改抓取频率

编辑 `.github/workflows/news-aggregator.yml`：

```yaml
schedule:
  # 每天 8:00, 12:00, 18:00 (UTC时间)
  - cron: '0 0,4,10 * * *'
```

**时区转换**：
- UTC+8（北京时间）：0:00, 4:00, 10:00 UTC = 8:00, 12:00, 18:00 北京时间

### 添加新闻源

编辑 `config.yaml`：

```yaml
news_sources:
  tech:
    - name: "新网站"
      url: "https://example.com"
      selector: ".news-item"
      link_selector: "a"
      title_selector: ".title"
      desc_selector: ".desc"
      enabled: true
```

### 修改主题

编辑 `config.yaml`：

```yaml
html:
  theme: "modern"  # 可选: modern, dark, minimal
```

## 常见问题

### Q: 为什么没有抓取到新闻？

A: 可能原因：
1. 新闻源网站不可访问
2. CSS 选择器不匹配
3. 网络问题
4. 反爬虫机制

**解决方法**：
1. 检查新闻源 URL 是否可访问
2. 更新 CSS 选择器
3. 增加请求延迟
4. 检查 GitHub Actions 日志

### Q: 如何查看运行日志？

A: 
1. 进入 GitHub 仓库的 Actions 标签页
2. 点击最近的运行
3. 查看详细日志

### Q: 如何自定义域名？

A:
1. 在 `docs/` 目录创建 `CNAME` 文件，内容为你的域名
2. 在域名提供商处添加 DNS 记录
3. 等待 DNS 生效（通常几分钟到几小时）

### Q: 如何添加通知？

A: 编辑 `config.yaml`：

```yaml
notifications:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
```

## 下一步

- 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 获取详细部署指南
- 查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解如何贡献代码
- 查看 [README.md](README.md) 了解项目详情

## 需要帮助？

- 创建 Issue：https://github.com/your-username/news-aggregator/issues
- 查看 Discussions：https://github.com/your-username/news-aggregator/discussions