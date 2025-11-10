"""
MCP Web Search Tool
一个用于搜索网页最新内容的MCP工具
"""

import json
import requests
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from urllib.parse import quote_plus, urlparse
import time
from bs4 import BeautifulSoup


class MCPSearchTool:
    """MCP网页搜索工具类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def search_web(self, query: str, num_results: int = 10, time_range: str = "d") -> Dict[str, Any]:
        """
        搜索网页内容
        
        Args:
            query: 搜索关键词
            num_results: 返回结果数量 (默认10)
            time_range: 时间范围 (d=天, w=周, m=月, y=年)
            
        Returns:
            包含搜索结果的词典
        """
        try:
            # 使用Google搜索API (模拟搜索)
            search_results = self._google_search(query, num_results, time_range)
            
            # 提取和解析内容
            parsed_results = []
            for result in search_results:
                content = self._extract_content(result['url'])
                parsed_results.append({
                    'title': result.get('title', ''),
                    'url': result['url'],
                    'snippet': result.get('snippet', ''),
                    'content': content,
                    'timestamp': datetime.now().isoformat()
                })
                
                # 添加延迟避免请求过快
                time.sleep(0.5)
            
            return {
                'status': 'success',
                'query': query,
                'num_results': len(parsed_results),
                'results': parsed_results,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                'query': query,
                'timestamp': datetime.now().isoformat()
            }
    
    def _google_search(self, query: str, num_results: int, time_range: str) -> List[Dict[str, str]]:
        """
        模拟Google搜索 (实际项目中可以使用SerpAPI或其他搜索API)
        """
        # 这里使用一个简化的搜索模拟
        # 在实际应用中，您需要集成真实的搜索API
        
        # 模拟搜索结果
        mock_results = [
            {
                'title': f'关于 "{query}" 的最新消息 - 新闻网站1',
                'url': f'https://example-news1.com/{quote_plus(query)}',
                'snippet': f'最新的 {query} 相关信息和新闻报道...'
            },
            {
                'title': f'{query} - 维基百科',
                'url': f'https://zh.wikipedia.org/wiki/{quote_plus(query)}',
                'snippet': f'{query} 的定义、历史和最新发展...'
            },
            {
                'title': f'深度解析: {query} 的现状与趋势',
                'url': f'https://tech-blog.com/{quote_plus(query)}',
                'snippet': f'专家分析 {query} 的最新趋势和未来发展方向...'
            }
        ]
        
        return mock_results[:num_results]
    
    def _extract_content(self, url: str) -> str:
        """
        从网页提取主要内容
        """
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # 移除脚本和样式标签
            for script in soup(["script", "style"]):
                script.decompose()
            
            # 提取主要内容
            content = ''
            
            # 尝试不同的内容选择器
            content_selectors = [
                'article',
                'main',
                '.content',
                '.article-content',
                '.post-content',
                '#content',
                '.entry-content'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True, separator=' ')
                    break
            
            # 如果没有找到特定内容区域，获取所有段落
            if not content:
                paragraphs = soup.find_all('p')
                content = ' '.join([p.get_text(strip=True) for p in paragraphs[:5]])
            
            # 限制内容长度
            if len(content) > 2000:
                content = content[:2000] + '...'
            
            return content
            
        except Exception as e:
            return f"无法提取内容: {str(e)}"
    
    def search_news(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        专门搜索新闻内容
        """
        # 在查询中添加新闻相关的关键词
        news_query = f"{query} 新闻 最新 报道"
        return self.search_web(news_query, num_results, time_range="d")
    
    def search_tech(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        """
        搜索技术相关内容
        """
        tech_query = f"{query} 技术 开发 教程"
        return self.search_web(tech_query, num_results, time_range="w")
    
    def get_tool_info(self) -> Dict[str, Any]:
        """
        获取工具信息
        """
        return {
            "name": "MCP Web Search Tool",
            "version": "1.0.0",
            "description": "搜索网页最新内容的MCP工具",
            "functions": [
                "search_web - 通用网页搜索",
                "search_news - 新闻搜索",
                "search_tech - 技术内容搜索"
            ],
            "author": "AI Assistant"
        }


# MCP工具接口函数
def search_web_content(query: str, num_results: int = 10, time_range: str = "d") -> str:
    """
    MCP工具主函数 - 搜索网页内容
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
        time_range: 时间范围 (d=天, w=周, m=月, y=年)
        
    Returns:
        JSON格式的搜索结果
    """
    tool = MCPSearchTool()
    results = tool.search_web(query, num_results, time_range)
    return json.dumps(results, ensure_ascii=False, indent=2)


def search_latest_news(query: str, num_results: int = 5) -> str:
    """
    MCP工具函数 - 搜索最新新闻
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
        
    Returns:
        JSON格式的新闻搜索结果
    """
    tool = MCPSearchTool()
    results = tool.search_news(query, num_results)
    return json.dumps(results, ensure_ascii=False, indent=2)


def search_tech_content(query: str, num_results: int = 5) -> str:
    """
    MCP工具函数 - 搜索技术内容
    
    Args:
        query: 搜索关键词
        num_results: 返回结果数量
        
    Returns:
        JSON格式的技术搜索结果
    """
    tool = MCPSearchTool()
    results = tool.search_tech(query, num_results)
    return json.dumps(results, ensure_ascii=False, indent=2)


def get_search_tool_info() -> str:
    """
    获取搜索工具信息
    
    Returns:
        JSON格式的工具信息
    """
    tool = MCPSearchTool()
    info = tool.get_tool_info()
    return json.dumps(info, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 测试工具
    print("MCP搜索工具测试")
    print("=" * 50)
    
    # 测试基本信息
    print("工具信息:")
    print(get_search_tool_info())
    print()
    
    # 测试网页搜索
    print("网页搜索测试 (人工智能):")
    result = search_web_content("人工智能", num_results=3)
    print(result)
    print()
    
    # 测试新闻搜索
    print("新闻搜索测试 (机器学习):")
    result = search_latest_news("机器学习", num_results=2)
    print(result)