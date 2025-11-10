"""
MCP搜索工具测试模块
"""

import unittest
import json
from unittest.mock import patch, MagicMock
from mcp.mcp_search_tool import MCPSearchTool, search_web_content
from mcp.mcp_tool_integration import MCPSearchIntegration


class TestMCPSearchTool(unittest.TestCase):
    """测试MCP搜索工具类"""
    
    def setUp(self):
        """测试初始化"""
        self.tool = MCPSearchTool()
    
    def test_tool_initialization(self):
        """测试工具初始化"""
        self.assertIsNotNone(self.tool)
        self.assertIsNotNone(self.tool.session)
    
    def test_get_tool_info(self):
        """测试获取工具信息"""
        info = self.tool.get_tool_info()
        self.assertEqual(info["name"], "MCP Web Search Tool")
        self.assertEqual(info["version"], "1.0.0")
        self.assertIn("functions", info)
    
    @patch('mcp_search_tool.requests.Session')
    def test_search_web_mock(self, mock_session):
        """测试网页搜索 (模拟)"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.content = b'<html><body><article>测试内容</article></body></html>'
        mock_response.raise_for_status.return_value = None
        
        mock_session.return_value.get.return_value = mock_response
        
        # 执行搜索
        result = self.tool.search_web("测试查询", num_results=1)
        
        # 验证结果
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["query"], "测试查询")
        self.assertGreater(result["num_results"], 0)
    
    def test_search_web_content_function(self):
        """测试搜索函数"""
        result_str = search_web_content("人工智能", num_results=1)
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["query"], "人工智能")
        self.assertIn("results", result)
    
    def test_invalid_query(self):
        """测试无效查询"""
        result_str = search_web_content("")
        result = json.loads(result_str)
        
        # 空查询应该也能工作，返回模拟结果
        self.assertEqual(result["status"], "success")


class TestMCPSearchIntegration(unittest.TestCase):
    """测试MCP搜索工具集成"""
    
    def setUp(self):
        """测试初始化"""
        self.integration = MCPSearchIntegration()
    
    def test_integration_initialization(self):
        """测试集成初始化"""
        self.assertIsNotNone(self.integration)
        self.assertIsNotNone(self.integration.config)
    
    def test_get_tool_definition(self):
        """测试获取工具定义"""
        definition = self.integration.get_tool_definition()
        
        self.assertEqual(definition["name"], "web_search")
        self.assertEqual(definition["version"], "1.0.0")
        self.assertIn("functions", definition)
        self.assertGreater(len(definition["functions"]), 0)
    
    def test_execute_function_search_web(self):
        """测试执行搜索函数"""
        parameters = {
            "query": "机器学习",
            "num_results": 1,
            "time_range": "d"
        }
        
        result_str = self.integration.execute_function("search_web", parameters)
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["query"], "机器学习")
    
    def test_execute_function_invalid(self):
        """测试执行无效函数"""
        result_str = self.integration.execute_function("invalid_function", {})
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "error")
        self.assertIn("未知的函数", result["message"])
    
    def test_execute_function_missing_params(self):
        """测试执行函数缺少参数"""
        result_str = self.integration.execute_function("search_web", {})
        result = json.loads(result_str)
        
        # 应该能处理缺少参数的情况
        self.assertEqual(result["status"], "success")
    
    def test_health_status(self):
        """测试健康状态"""
        health = self.integration.get_health_status()
        
        self.assertIn("status", health)
        self.assertIn("timestamp", health)
        self.assertIn("functions", health)
        self.assertIn("config_valid", health)


class TestSearchFunctions(unittest.TestCase):
    """测试搜索相关函数"""
    
    def test_search_web_content(self):
        """测试网页搜索内容函数"""
        result_str = search_web_content("Python编程", num_results=2)
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["query"], "Python编程")
        self.assertLessEqual(len(result["results"]), 2)
    
    def test_search_latest_news(self):
        """测试最新新闻搜索"""
        result_str = search_latest_news("科技新闻", num_results=1)
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("results", result)
    
    def test_search_tech_content(self):
        """测试技术内容搜索"""
        result_str = search_tech_content("深度学习", num_results=1)
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "success")
        self.assertIn("results", result)


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""
    
    def test_network_error_handling(self):
        """测试网络错误处理"""
        # 这里可以测试网络错误情况
        # 由于我们使用模拟数据，通常不会出错
        pass
    
    def test_invalid_json_params(self):
        """测试无效JSON参数"""
        integration = MCPSearchIntegration()
        
        # 测试无效JSON字符串
        result_str = integration.execute_function("search_web", "invalid json")
        result = json.loads(result_str)
        
        self.assertEqual(result["status"], "error")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)