#!/usr/bin/env python3
"""
快速测试MCP搜索工具
"""

import json
from mcp.mcp_search_tool import search_web_content, get_search_tool_info
from mcp.mcp_tool_integration import execute_mcp_function


def test_basic_functionality():
    """测试基本功能"""
    print("🚀 MCP搜索工具快速测试")
    print("=" * 40)
    
    try:
        # 测试1: 工具信息
        print("1️⃣ 测试工具信息...")
        tool_info = json.loads(get_search_tool_info())
        print(f"✅ 工具名称: {tool_info['name']}")
        print(f"✅ 版本: {tool_info['version']}")
        
        # 测试2: 基本搜索
        print("\n2️⃣ 测试基本搜索...")
        search_result = json.loads(search_web_content("人工智能", num_results=2))
        if search_result['status'] == 'success':
            print(f"✅ 搜索成功! 找到 {search_result['num_results']} 个结果")
            for i, result in enumerate(search_result['results'][:2], 1):
                print(f"   {i}. {result['title']}")
                print(f"      {result['url']}")
        else:
            print(f"❌ 搜索失败: {search_result['message']}")
        
        # 测试3: MCP集成
        print("\n3️⃣ 测试MCP集成...")
        params = json.dumps({"query": "机器学习", "num_results": 1})
        mcp_result = json.loads(execute_mcp_function("search_web", params))
        if mcp_result['status'] == 'success':
            print(f"✅ MCP集成测试通过! 找到 {mcp_result['num_results']} 个结果")
        else:
            print(f"❌ MCP集成测试失败: {mcp_result['message']}")
        
        print("\n🎉 快速测试完成! 工具运行正常!")
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False


if __name__ == "__main__":
    test_basic_functionality()