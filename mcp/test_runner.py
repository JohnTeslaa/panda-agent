#!/usr/bin/env python3
"""
简单测试运行器
"""

import sys
import subprocess

def install_dependencies():
    """安装依赖"""
    print("安装依赖包...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', 
            'requests', 'beautifulsoup4', 'lxml', 'urllib3'
        ], check=True)
        print("✅ 依赖包安装完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依赖包安装失败")
        return False

def run_quick_test():
    """运行快速测试"""
    print("运行快速测试...")
    try:
        result = subprocess.run([
            sys.executable, 'quick_test.py'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("错误输出:", result.stderr)
        
        return result.returncode == 0
    except Exception as e:
        print(f"测试运行失败: {e}")
        return False

def main():
    print("MCP搜索工具测试运行器")
    print("=" * 40)
    
    # 安装依赖
    if not install_dependencies():
        return False
    
    # 运行测试
    success = run_quick_test()
    
    if success:
        print("\n🎉 测试通过! 可以运行演示程序:")
        print("python demo.py")
    else:
        print("\n❌ 测试失败，请检查错误信息")
    
    return success

if __name__ == "__main__":
    main()