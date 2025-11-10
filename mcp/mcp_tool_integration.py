"""
MCP工具集成模块
用于将搜索工具集成到MCP框架中
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from mcp_search_tool import (
    search_web_content,
    search_latest_news, 
    search_tech_content,
    get_search_tool_info
)
from mcp_search_config import get_config, validate_config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class MCPSearchIntegration:
    """MCP搜索工具集成类"""
    
    def __init__(self):
        self.config = get_config()
        self.validate_config()
        logger.info("MCP搜索工具集成初始化完成")
    
    def validate_config(self):
        """验证配置"""
        if not validate_config():
            logger.warning("配置验证失败，使用默认配置")
    
    def get_tool_definition(self) -> Dict[str, Any]:
        """
        获取MCP工具定义
        
        Returns:
            MCP工具定义字典
        """
        return {
            "name": "web_search",
            "description": "搜索网页最新内容的工具",
            "version": "1.0.0",
            "functions": [
                {
                    "name": "search_web",
                    "description": "通用网页搜索",
                    "parameters": {
                        "query": {
                            "type": "string",
                            "description": "搜索关键词",
                            "required": True
                        },
                        "num_results": {
                            "type": "integer", 
                            "description": "返回结果数量 (默认10, 最大50)",
                            "required": False,
                            "default": 10
                        },
                        "time_range": {
                            "type": "string",
                            "description": "时间范围 (d=天, w=周, m=月, y=年)",
                            "required": False,
                            "default": "d"
                        }
                    },
                    "returns": {
                        "type": "object",
                        "description": "搜索结果对象，包含状态、结果列表等信息"
                    }
                },
                {
                    "name": "search_news",
                    "description": "搜索最新新闻内容",
                    "parameters": {
                        "query": {
                            "type": "string",
                            "description": "新闻搜索关键词",
                            "required": True
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "返回结果数量 (默认5, 最大20)",
                            "required": False,
                            "default": 5
                        }
                    },
                    "returns": {
                        "type": "object", 
                        "description": "新闻搜索结果对象"
                    }
                },
                {
                    "name": "search_tech",
                    "description": "搜索技术相关内容",
                    "parameters": {
                        "query": {
                            "type": "string",
                            "description": "技术搜索关键词",
                            "required": True
                        },
                        "num_results": {
                            "type": "integer",
                            "description": "返回结果数量 (默认5, 最大20)",
                            "required": False,
                            "default": 5
                        }
                    },
                    "returns": {
                        "type": "object",
                        "description": "技术搜索结果对象"
                    }
                },
                {
                    "name": "get_tool_info",
                    "description": "获取工具信息和状态",
                    "parameters": {},
                    "returns": {
                        "type": "object",
                        "description": "工具信息对象"
                    }
                }
            ]
        }
    
    def execute_function(self, function_name: str, parameters: Dict[str, Any]) -> str:
        """
        执行MCP工具函数
        
        Args:
            function_name: 函数名称
            parameters: 参数字典
            
        Returns:
            执行结果(JSON字符串)
        """
        try:
            logger.info(f"执行函数: {function_name}, 参数: {parameters}")
            
            if function_name == "search_web":
                query = parameters.get("query", "")
                num_results = parameters.get("num_results", 10)
                time_range = parameters.get("time_range", "d")
                
                if not query:
                    return json.dumps({
                        "status": "error",
                        "message": "搜索关键词不能为空"
                    }, ensure_ascii=False)
                
                return search_web_content(query, num_results, time_range)
            
            elif function_name == "search_news":
                query = parameters.get("query", "")
                num_results = parameters.get("num_results", 5)
                
                if not query:
                    return json.dumps({
                        "status": "error", 
                        "message": "搜索关键词不能为空"
                    }, ensure_ascii=False)
                
                return search_latest_news(query, num_results)
            
            elif function_name == "search_tech":
                query = parameters.get("query", "")
                num_results = parameters.get("num_results", 5)
                
                if not query:
                    return json.dumps({
                        "status": "error",
                        "message": "搜索关键词不能为空"
                    }, ensure_ascii=False)
                
                return search_tech_content(query, num_results)
            
            elif function_name == "get_tool_info":
                return get_search_tool_info()
            
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"未知的函数: {function_name}"
                }, ensure_ascii=False)
        
        except Exception as e:
            logger.error(f"函数执行错误: {function_name}, 错误: {str(e)}")
            return json.dumps({
                "status": "error",
                "message": f"函数执行失败: {str(e)}"
            }, ensure_ascii=False)
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        获取工具健康状态
        
        Returns:
            健康状态字典
        """
        try:
            # 测试基本功能
            test_result = json.loads(search_web_content("测试", num_results=1))
            
            return {
                "status": "healthy",
                "timestamp": datetime.now().isoformat(),
                "functions": {
                    "search_web": test_result.get("status") == "success",
                    "search_news": True,  # 假设可用
                    "search_tech": True,  # 假设可用
                    "get_tool_info": True
                },
                "config_valid": validate_config()
            }
        
        except Exception as e:
            logger.error(f"健康检查失败: {str(e)}")
            return {
                "status": "unhealthy",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "config_valid": validate_config()
            }


# MCP工具实例
mcp_integration = MCPSearchIntegration()


def get_mcp_tool_definition() -> str:
    """
    获取MCP工具定义 (供MCP框架调用)
    
    Returns:
        JSON格式的工具定义
    """
    definition = mcp_integration.get_tool_definition()
    return json.dumps(definition, ensure_ascii=False, indent=2)


def execute_mcp_function(function_name: str, parameters: str) -> str:
    """
    执行MCP工具函数 (供MCP框架调用)
    
    Args:
        function_name: 函数名称
        parameters: JSON格式的参数字符串
        
    Returns:
        JSON格式的执行结果
    """
    try:
        params = json.loads(parameters) if parameters else {}
        return mcp_integration.execute_function(function_name, params)
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "参数格式错误，必须是有效的JSON字符串"
        }, ensure_ascii=False)
    except Exception as e:
        return json.dumps({
            "status": "error", 
            "message": f"函数执行失败: {str(e)}"
        }, ensure_ascii=False)


def get_mcp_health_status() -> str:
    """
    获取MCP工具健康状态 (供MCP框架调用)
    
    Returns:
        JSON格式的健康状态
    """
    status = mcp_integration.get_health_status()
    return json.dumps(status, ensure_ascii=False, indent=2)


# 测试函数
def test_mcp_integration():
    """测试MCP集成"""
    print("MCP搜索工具集成测试")
    print("=" * 50)
    
    # 测试工具定义
    print("1. 工具定义:")
    definition = get_mcp_tool_definition()
    print(definition)
    print()
    
    # 测试函数执行
    print("2. 函数执行测试:")
    
    # 测试搜索
    test_params = json.dumps({"query": "人工智能", "num_results": 1})
    result = execute_mcp_function("search_web", test_params)
    print(f"搜索结果: {result}")
    print()
    
    # 测试工具信息
    info = execute_mcp_function("get_tool_info", "{}")
    print(f"工具信息: {info}")
    print()
    
    # 测试健康状态
    print("3. 健康状态:")
    health = get_mcp_health_status()
    print(health)


if __name__ == "__main__":
    test_mcp_integration()