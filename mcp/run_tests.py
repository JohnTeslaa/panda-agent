#!/usr/bin/env python3
"""
MCP搜索工具测试运行器
"""

import subprocess
import sys
import json
from mcp.mcp_search_tool import get_search_tool_info
from mcp.mcp_tool_integration import get_mcp_health_status


def run_unit_tests():
    """运行单元测试"""
    print("运行单元测试...")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'unittest', 
            'test_mcp_search', '-v'
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"运行测试失败: {e}")
        return False


def run_integration_test():
    """运行集成测试"""
    print("运行集成测试...")
    try:
        # 测试工具信息
        print("1. 测试工具信息...")
        tool_info = json.loads(get_search_tool_info())
        assert tool_info["name"] == "MCP Web Search Tool"
        print("✓ 工具信息测试通过")
        
        # 测试健康状态
        print("2. 测试健康状态...")
        health_status = json.loads(get_mcp_health_status())
        assert health_status["status"] in ["healthy", "unhealthy"]
        print("✓ 健康状态测试通过")
        
        # 测试搜索功能
        print("3. 测试搜索功能...")
        from mcp.mcp_search_tool import search_web_content
        search_result = json.loads(search_web_content("测试", num_results=1))
        assert search_result["status"] == "success"
        assert len(search_result["results"]) > 0
        print("✓ 搜索功能测试通过")
        
        print("集成测试全部通过!")
        return True
        
    except Exception as e:
        print(f"集成测试失败: {e}")
        return False


def run_examples():
    """运行示例代码"""
    print("运行示例代码...")
    try:
        result = subprocess.run([
            sys.executable, 'mcp_search_example.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("示例代码运行成功!")
            return True
        else:
            print("示例代码运行失败:")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("示例代码运行超时")
        return False
    except Exception as e:
        print(f"运行示例代码失败: {e}")
        return False


def check_dependencies():
    """检查依赖包"""
    print("检查依赖包...")
    required_packages = [
        'requests', 'beautifulsoup4', 'lxml', 'urllib3'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"缺少依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("✓ 所有依赖包已安装")
        return True


def main():
    """主函数"""
    print("MCP搜索工具测试运行器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return False
    
    all_passed = True
    
    # 运行单元测试
    if not run_unit_tests():
        print("单元测试未完全通过")
        all_passed = False
    
    print()
    
    # 运行集成测试
    if not run_integration_test():
        print("集成测试未通过")
        all_passed = False
    
    print()
    
    # 运行示例
    if not run_examples():
        print("示例代码运行失败")
        all_passed = False
    
    print()
    print("=" * 50)
    
    if all_passed:
        print("🎉 所有测试通过! MCP搜索工具已就绪!")
        return True
    else:
        print("⚠️  部分测试未通过，请检查输出信息")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)