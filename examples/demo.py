#!/usr/bin/env python3
"""
灵魂伴侣 Agent 使用示例
演示如何在代码中使用Agent
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from soul_mate import SoulMateAgent


def demo_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例 1: 基本使用")
    print("=" * 60)
    
    # 创建Agent实例
    agent = SoulMateAgent(user_id="demo_user", model="gpt-4.1-mini")
    
    # 发送请求
    response = agent.chat("我想学习Python编程，有什么适合初学者的书籍推荐吗？")
    print(response)
    print()


def demo_conversation():
    """对话示例"""
    print("=" * 60)
    print("示例 2: 多轮对话")
    print("=" * 60)
    
    agent = SoulMateAgent(user_id="demo_user_2", model="gpt-4.1-mini")
    
    # 第一轮对话
    print("用户: 我喜欢科幻小说")
    response1 = agent.chat("我喜欢科幻小说")
    print(f"Agent: {response1[:200]}...\n")
    
    # 第二轮对话
    print("用户: 推荐一些刘慈欣的作品")
    response2 = agent.chat("推荐一些刘慈欣的作品")
    print(f"Agent: {response2[:200]}...\n")


def demo_programmatic_access():
    """程序化访问示例"""
    print("=" * 60)
    print("示例 3: 程序化访问推荐结果")
    print("=" * 60)
    
    agent = SoulMateAgent(user_id="demo_user_3", model="gpt-4.1-mini")
    
    # 获取推荐结果（返回结构化数据）
    result = agent.recommend("推荐一些关于人工智能的书籍", top_k=3)
    
    if result["success"]:
        print(f"找到 {len(result['recommendations'])} 个推荐：\n")
        
        for i, rec in enumerate(result["recommendations"], 1):
            print(f"{i}. {rec.get('title', 'Unknown')}")
            print(f"   作者: {rec.get('author', 'Unknown')}")
            print(f"   评分: {rec.get('score', 'N/A')}/10")
            print()
        
        # 模拟用户反馈
        if result["recommendations"]:
            first_rec = result["recommendations"][0]
            agent.feedback(
                item_id=first_rec.get("title", "unknown"),
                liked=True,
                item_info=first_rec
            )
            print("✓ 已记录用户反馈")
    else:
        print(result["message"])


def demo_user_profile():
    """用户画像示例"""
    print("=" * 60)
    print("示例 4: 用户画像管理")
    print("=" * 60)
    
    agent = SoulMateAgent(user_id="demo_user_4", model="gpt-4.1-mini")
    
    # 手动添加偏好
    agent.user_profile.add_genre("科幻")
    agent.user_profile.add_genre("推理")
    agent.user_profile.add_topic("人工智能")
    agent.user_profile.add_topic("量子计算")
    agent.user_profile.add_author("刘慈欣")
    agent.user_profile.update_preferences(reading_level="advanced")
    
    # 查看用户画像
    print("用户画像摘要：")
    print(agent.user_profile.get_profile_summary())
    print()
    
    # 基于画像推荐
    response = agent.chat("给我推荐一些书")
    print(f"推荐结果（基于画像）：\n{response[:300]}...")


def main():
    """主函数"""
    print("\n🎯 灵魂伴侣 Agent 使用示例\n")
    
    try:
        # 运行各个示例
        demo_basic_usage()
        print("\n" + "="*60 + "\n")
        
        demo_conversation()
        print("\n" + "="*60 + "\n")
        
        demo_programmatic_access()
        print("\n" + "="*60 + "\n")
        
        demo_user_profile()
        
        print("\n" + "="*60)
        print("✓ 所有示例运行完成！")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 运行出错: {str(e)}")
        print("请确保已设置 OPENAI_API_KEY 环境变量")


if __name__ == "__main__":
    main()
