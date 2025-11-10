"""
MCP搜索工具使用示例
"""

import json
from mcp_search_tool import (
    search_web_content, 
    search_latest_news, 
    search_tech_content,
    get_search_tool_info
)


def example_basic_search():
    """基础搜索示例"""
    print("=== 基础搜索示例 ===")
    
    # 搜索人工智能相关内容
    query = "人工智能最新发展"
    print(f"搜索查询: {query}")
    
    result = search_web_content(query, num_results=3)
    parsed_result = json.loads(result)
    
    if parsed_result['status'] == 'success':
        print(f"找到 {parsed_result['num_results']} 个结果:")
        for i, item in enumerate(parsed_result['results'], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   URL: {item['url']}")
            print(f"   摘要: {item['snippet']}")
            print(f"   内容预览: {item['content'][:100]}...")
    else:
        print(f"搜索失败: {parsed_result['message']}")
    
    print("\n" + "="*50 + "\n")


def example_news_search():
    """新闻搜索示例"""
    print("=== 新闻搜索示例 ===")
    
    # 搜索最新科技新闻
    query = "ChatGPT"
    print(f"新闻搜索: {query}")
    
    result = search_latest_news(query, num_results=2)
    parsed_result = json.loads(result)
    
    if parsed_result['status'] == 'success':
        print(f"找到 {parsed_result['num_results']} 条新闻:")
        for i, item in enumerate(parsed_result['results'], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   来源: {item['url']}")
            print(f"   摘要: {item['snippet']}")
            print(f"   获取时间: {item['timestamp']}")
    else:
        print(f"搜索失败: {parsed_result['message']}")
    
    print("\n" + "="*50 + "\n")


def example_tech_search():
    """技术内容搜索示例"""
    print("=== 技术内容搜索示例 ===")
    
    # 搜索技术教程
    query = "Python机器学习"
    print(f"技术搜索: {query}")
    
    result = search_tech_content(query, num_results=2)
    parsed_result = json.loads(result)
    
    if parsed_result['status'] == 'success':
        print(f"找到 {parsed_result['num_results']} 个技术资源:")
        for i, item in enumerate(parsed_result['results'], 1):
            print(f"\n{i}. {item['title']}")
            print(f"   链接: {item['url']}")
            print(f"   简介: {item['snippet']}")
            print(f"   内容长度: {len(item['content'])} 字符")
    else:
        print(f"搜索失败: {parsed_result['message']}")
    
    print("\n" + "="*50 + "\n")


def example_multiple_searches():
    """多次搜索示例"""
    print("=== 多次搜索示例 ===")
    
    search_queries = [
        "量子计算最新进展",
        "区块链技术应用",
        "元宇宙发展趋势"
    ]
    
    all_results = {}
    
    for query in search_queries:
        print(f"正在搜索: {query}")
        result = search_web_content(query, num_results=2)
        parsed_result = json.loads(result)
        
        if parsed_result['status'] == 'success':
            all_results[query] = {
                'count': parsed_result['num_results'],
                'top_result': parsed_result['results'][0] if parsed_result['results'] else None
            }
            print(f"  ✓ 找到 {parsed_result['num_results']} 个结果")
        else:
            all_results[query] = {'error': parsed_result['message']}
            print(f"  ✗ 搜索失败: {parsed_result['message']}")
    
    print("\n搜索汇总:")
    for query, result in all_results.items():
        if 'error' in result:
            print(f"  {query}: 失败 - {result['error']}")
        else:
            top_title = result['top_result']['title'] if result['top_result'] else '无结果'
            print(f"  {query}: {result['count']} 个结果，首个: {top_title}")
    
    print("\n" + "="*50 + "\n")


def example_tool_info():
    """工具信息示例"""
    print("=== 工具信息 ===")
    
    info = get_search_tool_info()
    parsed_info = json.loads(info)
    
    print(f"工具名称: {parsed_info['name']}")
    print(f"版本: {parsed_info['version']}")
    print(f"描述: {parsed_info['description']}")
    print(f"作者: {parsed_info['author']}")
    print("功能列表:")
    for func in parsed_info['functions']:
        print(f"  - {func}")
    
    print("\n" + "="*50 + "\n")


def example_custom_search():
    """自定义搜索示例"""
    print("=== 自定义搜索示例 ===")
    
    # 不同时间范围的搜索
    queries = [
        ("人工智能", "d"),  # 最近一天
        ("区块链", "w"),    # 最近一周
        ("云计算", "m"),    # 最近一月
    ]
    
    for query, time_range in queries:
        print(f"搜索: {query} (时间范围: {time_range})")
        result = search_web_content(query, num_results=1, time_range=time_range)
        parsed_result = json.loads(result)
        
        if parsed_result['status'] == 'success' and parsed_result['results']:
            item = parsed_result['results'][0]
            print(f"  结果: {item['title']}")
            print(f"  URL: {item['url']}")
        else:
            print(f"  无结果或搜索失败")
        print()
    
    print("="*50 + "\n")


def main():
    """主函数 - 运行所有示例"""
    print("MCP搜索工具使用示例")
    print("=" * 60)
    
    try:
        # 运行各种示例
        example_tool_info()
        example_basic_search()
        example_news_search()
        example_tech_search()
        example_multiple_searches()
        example_custom_search()
        
        print("所有示例运行完成！")
        
    except Exception as e:
        print(f"运行示例时出错: {e}")
        print("请确保已安装所有依赖包:")
        print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()