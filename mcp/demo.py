#!/usr/bin/env python3
"""
MCP搜索工具演示
"""

import json
from mcp_search_tool import (
    search_web_content, 
    search_latest_news, 
    search_tech_content,
    get_search_tool_info
)


def format_search_results(results_json):
    """格式化搜索结果"""
    data = json.loads(results_json)
    
    if data['status'] != 'success':
        return f"搜索失败: {data.get('message', '未知错误')}"
    
    output = []
    output.append(f"🔍 搜索结果: {data['query']}")
    output.append(f"📊 找到 {data['num_results']} 个结果")
    output.append("-" * 50)
    
    for i, result in enumerate(data['results'], 1):
        output.append(f"\n{i}. {result['title']}")
        output.append(f"   🔗 {result['url']}")
        output.append(f"   📝 {result['snippet']}")
        if result.get('content'):
            content_preview = result['content'][:100] + "..." if len(result['content']) > 100 else result['content']
            output.append(f"   📄 {content_preview}")
    
    return "\n".join(output)


def main():
    """主演示函数"""
    print("🌟 MCP搜索工具演示")
    print("=" * 60)
    
    # 显示工具信息
    tool_info = json.loads(get_search_tool_info())
    print(f"工具: {tool_info['name']} v{tool_info['version']}")
    print(f"描述: {tool_info['description']}")
    print()
    
    # 演示1: 通用搜索
    print("🔍 演示1: 通用网页搜索")
    print("-" * 40)
    query1 = "量子计算最新突破"
    print(f"搜索: {query1}")
    results1 = search_web_content(query1, num_results=3)
    print(format_search_results(results1))
    print()
    
    # 演示2: 新闻搜索
    print("📰 演示2: 新闻搜索")
    print("-" * 40)
    query2 = "人工智能医疗应用"
    print(f"搜索: {query2}")
    results2 = search_latest_news(query2, num_results=2)
    print(format_search_results(results2))
    print()
    
    # 演示3: 技术搜索
    print("💻 演示3: 技术内容搜索")
    print("-" * 40)
    query3 = "Python机器学习教程"
    print(f"搜索: {query3}")
    results3 = search_tech_content(query3, num_results=2)
    print(format_search_results(results3))
    print()
    
    print("🎉 演示完成! 欢迎使用MCP搜索工具!")
    print("\n使用提示:")
    print("• 调整 num_results 参数控制结果数量")
    print("• 使用 time_range 参数控制时间范围 (d/w/m/y)")
    print("• 查看 README.md 获取更多使用方式")


if __name__ == "__main__":
    main()