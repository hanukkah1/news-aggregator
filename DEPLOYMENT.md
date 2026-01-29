# 部署指南

## 快速开始

### 1. Fork 本仓库

点击右上角的 "Fork" 按钮将本仓库复制到您的 GitHub 账户。

### 2. 启用 GitHub Pages

进入仓库设置：
- Settings → Pages → Source → Deploy from a branch
- 选择 `gh-pages` 分支和 `/ (root)` 目录
- 点击 Save

### 3. 手动触发首次运行

进入 Actions 标签页：
- 选择 "News Aggregator" workflow
- 点击 "Run workflow" 手动触发
- 等待运行完成（约 2-5 分钟）

### 4. 查看结果

运行完成后，访问：
- 主页面：`https://your-username.github.io/news-aggregator/`
- RSS订阅：`https://your-username.github.io/news-aggregator/rss/tech.xml`

## 本地运行

### 环境要求

- Python 3.9+
- 操作系统：Windows / macOS / Linux

### 安装依赖

```bash
# 克隆仓库
git clone https://github.com/your-username/news-aggregator.git
cd news-aggregator

# 安装依赖
pip install -r requirements.txt

# 可选：安装开发依赖
pip install -r requirements-dev.txt
```

### 本地测试

```bash
# 运行测试脚本
python test_local.py
```

### 运行主程序

```bash
# 使用默认配置
python src/main.py

# 指定配置文件
python src/main.py path/to/config.yaml

# 或者使用启动脚本
python run.py
```

## 配置说明

### 修改新闻源

编辑 `config.yaml` 文件：

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

### 修改抓取时间

编辑 `.github/workflows/news-aggregator.yml`：

```yaml
schedule:
  # 每天 8:00, 12:00, 18:00 (UTC时间)
  - cron: '0 0,4,10 * * *'
```

**注意**：GitHub Actions 使用 UTC 时间，需要根据您的时区调整：
- UTC+8（北京时间）：0:00, 4:00, 10:00 UTC = 8:00, 12:00, 18:00 北京时间

### 修改主题

编辑 `config.yaml`：

```yaml
html:
  theme: "modern"  # 可选: modern, dark, minimal
```

## 自定义域名

如果需要使用自定义域名：

1. 在 `docs/` 目录下创建 `CNAME` 文件：
   ```
   your-domain.com
   ```

2. 在域名提供商处添加 DNS 记录：
   - A 记录指向：`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - 或 CNAME 记录指向：`your-username.github.io`

## 故障排除

### 问题1：抓取失败

**原因**：新闻源网站可能有反爬虫机制

**解决方案**：
1. 检查新闻源 URL 是否可访问
2. 更新 User-Agent
3. 增加请求延迟
4. 考虑使用代理

### 问题2：RSS/HTML 生成失败

**原因**：解析规则不匹配

**解决方案**：
1. 检查新闻源的 HTML 结构
2. 更新 CSS 选择器
3. 在配置中禁用有问题的源

### 问题3：GitHub Actions 运行超时

**原因**：抓取的新闻源过多或网络问题

**解决方案**：
1. 减少新闻源数量
2. 增加超时时间
3. 分批运行

### 问题4：页面显示不正常

**原因**：CSS 样式问题或浏览器兼容性

**解决方案**：
1. 清除浏览器缓存
2. 尝试不同的浏览器
3. 检查 GitHub Pages 部署状态

## 高级配置

### 添加通知

编辑 `config.yaml`：

```yaml
notifications:
  telegram:
    enabled: true
    bot_token: "YOUR_BOT_TOKEN"
    chat_id: "YOUR_CHAT_ID"
```

### 自定义新闻源解析规则

支持多种解析方式：

```yaml
news_sources:
  tech:
    - name: "示例网站"
      url: "https://example.com"
      selector: ".news-item"  # CSS 选择器
      link_selector: "a"      # 链接选择器
      title_selector: ".title" # 标题选择器
      desc_selector: ".desc"   # 描述选择器
      enabled: true
```

### 数据保留策略

编辑 `config.yaml`：

```yaml
storage:
  keep_days: 30  # 保留30天的数据
  deduplicate: true  # 启用去重
```

## 维护

### 定期清理

GitHub Actions 会自动清理 30 天前的数据。如需手动清理：

```bash
# 清理旧数据
find data -name "*.json" -mtime +30 -delete
find logs -name "*.log" -mtime +30 -delete
```

### 更新依赖

```bash
# 更新 Python 依赖
pip install --upgrade -r requirements.txt

# 更新 GitHub Actions 依赖
# 修改 .github/workflows/news-aggregator.yml
```

### 监控运行状态

1. 查看 Actions 历史：`https://github.com/your-username/news-aggregator/actions`
2. 查看生成的文件：`https://github.com/your-username/news-aggregator/tree/gh-pages`
3. 查看日志：在 Actions 页面点击具体运行查看详细日志

## 贡献指南

欢迎贡献代码和新闻源！

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送分支：`git push origin feature/amazing-feature`
5. 创建 Pull Request

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件