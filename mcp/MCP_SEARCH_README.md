# MCP网页搜索工具

一个用于搜索网页最新内容的MCP(Model Context Protocol)工具，支持通用网页搜索、新闻搜索和技术内容搜索。

## 功能特性

- 🔍 **通用网页搜索** - 搜索各类网页内容
- 📰 **新闻搜索** - 专门搜索最新新闻
- 💻 **技术内容搜索** - 搜索技术教程和文档
- ⚡ **快速响应** - 优化的搜索和内容提取
- 🔧 **易于集成** - 标准的MCP工具接口
- 📊 **结构化结果** - JSON格式的搜索结果

## 安装

### 基本安装

```bash
# 克隆或下载代码后，安装依赖
pip install -r requirements.txt
```

### 可选的高级搜索功能

如果需要使用真实的搜索引擎API，可以安装额外的依赖：

```bash
# Google搜索API支持
pip install google-api-python-client

# SerpAPI搜索服务支持
pip install serpapi
```

## 快速开始

### 基本使用

```python
from mcp.mcp_search_tool import search_web_content

# 搜索网页内容
result = search_web_content("人工智能最新发展", num_results=5)
print(result)  # JSON格式的搜索结果
```

### 不同类型的搜索

```python
from mcp.mcp_search_tool import search_latest_news, search_tech_content

# 搜索新闻
news_result = search_latest_news("ChatGPT", num_results=3)

# 搜索技术内容
tech_result = search_tech_content("Python机器学习", num_results=3)
```

### MCP集成使用

```python
from mcp.mcp_tool_integration import execute_mcp_function

# 通过MCP接口执行搜索
parameters = '{"query": "深度学习", "num_results": 5}'
result = execute_mcp_function("search_web", parameters)
```

## API参考

### 主要函数

#### `search_web_content(query, num_results=10, time_range="d")`

通用网页搜索函数。

**参数:**
- `query` (str): 搜索关键词
- `num_results` (int): 返回结果数量 (默认10, 最大50)
- `time_range` (str): 时间范围 (d=天, w=周, m=月, y=年)

**返回:**
JSON字符串，包含搜索结果和元数据。

#### `search_latest_news(query, num_results=5)`

新闻搜索函数。

**参数:**
- `query` (str): 新闻搜索关键词
- `num_results` (int): 返回结果数量 (默认5, 最大20)

#### `search_tech_content(query, num_results=5)`

技术内容搜索函数。

**参数:**
- `query` (str): 技术搜索关键词
- `num_results` (int): 返回结果数量 (默认5, 最大20)

### MCP工具接口

#### `get_mcp_tool_definition()`

获取MCP工具定义。

#### `execute_mcp_function(function_name, parameters)`

执行MCP工具函数。

**参数:**
- `function_name` (str): 函数名称
- `parameters` (str): JSON格式的参数字符串

## 搜索结果格式

搜索结果以JSON格式返回，结构如下：

```json
{
  "status": "success",
  "query": "搜索关键词",
  "num_results": 5,
  "timestamp": "2024-01-01T12:00:00",
  "results": [
    {
      "title": "网页标题",
      "url": "https://example.com/page",
      "snippet": "网页摘要...",
      "content": "提取的网页内容...",
      "timestamp": "2024-01-01T12:00:00"
    }
  ]
}
```

## 配置

工具支持通过配置文件进行自定义：

```python
from mcp.mcp_search_config import update_config, validate_config

# 更新配置
update_config("default_num_results", 15)

# 验证配置
is_valid = validate_config()
```

### 环境变量

- `GOOGLE_SEARCH_API_KEY`: Google搜索API密钥
- `GOOGLE_SEARCH_ENGINE_ID`: Google搜索引擎ID
- `BING_SEARCH_API_KEY`: Bing搜索API密钥

## 高级配置

### 使用真实搜索API

默认情况下，工具使用模拟搜索结果。要使用真实的搜索API：

1. **Google搜索API**:
   ```python
   # 在mcp_search_config.py中配置
   SEARCH_CONFIG["search_engines"]["google"]["enabled"] = True
   SEARCH_CONFIG["search_engines"]["google"]["api_key"] = "YOUR_API_KEY"
   ```

2. **SerpAPI**:
   ```python
   # 安装serpapi包并配置
   import serpapi
   # 配置API密钥
   ```

### 自定义内容提取

可以自定义网页内容提取规则：

```python
# 在配置中添加自定义选择器
SEARCH_CONFIG["content_extractors"] = [
    'article',
    'main', 
    '.custom-content',
    '#main-content'
]
```

## 测试

运行测试套件：

```bash
# 运行所有测试
python test_mcp_search.py

# 运行特定测试类
python -m unittest test_mcp_search.TestMCPSearchTool
```

## 示例

查看 `mcp_search_example.py` 文件获取更多使用示例：

```bash
# 运行示例
python mcp_search_example.py
```

## 错误处理

工具包含完整的错误处理机制：

- **网络错误**: 自动重试和降级处理
- **超时错误**: 可配置的超时时间
- **解析错误**: 优雅的内容解析失败处理
- **API限制**: 请求频率控制和缓存机制

## 性能优化

- **请求缓存**: 支持结果缓存，减少重复请求
- **并发控制**: 限制并发请求数量
- **内容压缩**: 自动压缩提取的内容
- **智能重试**: 指数退避重试策略

## 贡献

欢迎提交Issue和Pull Request来改进这个工具。

## 许可证

MIT License - 详见LICENSE文件。

## 更新日志

### v1.0.0
- ✨ 初始版本发布
- 🔍 基础网页搜索功能
- 📰 新闻搜索功能  
- 💻 技术内容搜索功能
- 🔧 MCP工具集成
- ✅ 完整的测试套件