#!/usr/bin/env python3
"""
灵魂伴侣 Agent 主程序入口
"""

import os
import sys
import argparse
from soul_mate import SoulMateAgent


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="灵魂伴侣 - 个性化阅读推荐Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python main.py                    # 使用默认用户ID启动
  python main.py --user alice       # 使用指定用户ID启动
  python main.py --model gpt-4.1-mini  # 使用指定模型
        """
    )
    
    parser.add_argument(
        "--user",
        type=str,
        default="default_user",
        help="用户ID（默认: default_user）"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4.1-mini",
        help="LLM模型名称（默认: gpt-4.1-mini）"
    )
    
    args = parser.parse_args()
    
    # 检查环境变量
    if not os.getenv("OPENAI_API_KEY"):
        print("错误: 未设置 OPENAI_API_KEY 环境变量")
        print("请设置环境变量后再运行，例如:")
        print("  export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)
    
    # 创建Agent实例
    try:
        agent = SoulMateAgent(user_id=args.user, model=args.model)
        
        # 运行交互式界面
        agent.run_interactive()
        
    except Exception as e:
        print(f"启动失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
