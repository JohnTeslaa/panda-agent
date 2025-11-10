"""
MCP搜索工具配置文件
"""

import os
from typing import Dict, Any

# 搜索配置
SEARCH_CONFIG = {
    # 默认搜索参数
    "default_num_results": 10,
    "default_time_range": "d",  # d=天, w=周, m=月, y=年
    "max_num_results": 50,
    "request_timeout": 10,
    "request_delay": 0.5,  # 请求间隔(秒)
    
    # 内容提取配置
    "content_extractors": [
        'article',
        'main',
        '.content',
        '.article-content',
        '.post-content',
        '#content',
        '.entry-content'
    ],
    "max_content_length": 2000,
    "min_content_length": 100,
    
    # 搜索源配置
    "search_engines": {
        "google": {
            "enabled": True,
            "api_key": os.getenv("GOOGLE_SEARCH_API_KEY", ""),
            "search_engine_id": os.getenv("GOOGLE_SEARCH_ENGINE_ID", ""),
            "base_url": "https://www.googleapis.com/customsearch/v1"
        },
        "bing": {
            "enabled": False,
            "api_key": os.getenv("BING_SEARCH_API_KEY", ""),
            "base_url": "https://api.bing.microsoft.com/v7.0/search"
        }
    },
    
    # 用户代理列表
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ],
    
    # 缓存配置
    "cache": {
        "enabled": True,
        "ttl": 3600,  # 缓存时间(秒)
        "max_size": 1000  # 最大缓存条目数
    }
}

# 搜索类型配置
SEARCH_TYPES = {
    "web": {
        "description": "通用网页搜索",
        "time_range": "d",
        "num_results": 10
    },
    "news": {
        "description": "新闻搜索",
        "time_range": "d",
        "num_results": 5,
        "query_suffix": " 新闻 最新 报道"
    },
    "tech": {
        "description": "技术内容搜索",
        "time_range": "w",
        "num_results": 5,
        "query_suffix": " 技术 开发 教程"
    },
    "academic": {
        "description": "学术搜索",
        "time_range": "m",
        "num_results": 5,
        "query_suffix": " 论文 研究 学术"
    }
}

# 错误消息配置
ERROR_MESSAGES = {
    "network_error": "网络连接错误，请检查网络连接",
    "timeout_error": "请求超时，请稍后重试",
    "parse_error": "内容解析失败",
    "api_error": "搜索API错误",
    "rate_limit_error": "请求频率过高，请稍后重试",
    "invalid_query": "无效的搜索查询"
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "mcp_search_tool.log",
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5
}

def get_config() -> Dict[str, Any]:
    """获取完整配置"""
    return {
        "search": SEARCH_CONFIG,
        "search_types": SEARCH_TYPES,
        "errors": ERROR_MESSAGES,
        "logging": LOGGING_CONFIG
    }

def update_config(config_name: str, value: Any) -> None:
    """更新配置项"""
    if config_name in SEARCH_CONFIG:
        SEARCH_CONFIG[config_name] = value
    elif config_name in SEARCH_TYPES:
        SEARCH_TYPES[config_name] = value
    elif config_name in ERROR_MESSAGES:
        ERROR_MESSAGES[config_name] = value
    elif config_name in LOGGING_CONFIG:
        LOGGING_CONFIG[config_name] = value

def validate_config() -> bool:
    """验证配置有效性"""
    try:
        # 检查必要配置
        if SEARCH_CONFIG["default_num_results"] <= 0:
            return False
        
        if SEARCH_CONFIG["max_num_results"] < SEARCH_CONFIG["default_num_results"]:
            return False
        
        if SEARCH_CONFIG["request_timeout"] <= 0:
            return False
        
        # 检查搜索源配置
        for engine, config in SEARCH_CONFIG["search_engines"].items():
            if config["enabled"] and not config.get("api_key"):
                print(f"警告: {engine}搜索API密钥未配置")
        
        return True
        
    except Exception as e:
        print(f"配置验证错误: {e}")
        return False

# 初始化时验证配置
if __name__ == "__main__":
    if validate_config():
        print("配置验证通过")
    else:
        print("配置验证失败")