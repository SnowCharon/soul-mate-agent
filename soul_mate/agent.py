"""
灵魂伴侣 Agent 主类
整合所有模块，提供统一的交互接口
"""

from typing import List, Dict, Optional
from .user_profile import UserProfile
from .llm_client import LLMClient
from .content_fetcher import ContentFetcher


class SoulMateAgent:
    """灵魂伴侣推荐Agent"""
    
    def __init__(self, user_id: str = "default_user", model: str = "gpt-4.1-mini"):
        """
        初始化Agent
        
        Args:
            user_id: 用户ID
            model: LLM模型名称
        """
        self.user_profile = UserProfile(user_id)
        self.llm_client = LLMClient(model)
        self.content_fetcher = ContentFetcher()
        self.conversation_history = []
    
    def welcome(self) -> str:
        """欢迎信息"""
        if self.user_profile.is_new_user():
            return """欢迎使用灵魂伴侣推荐系统！ 📚

我是你的个性化阅读推荐助手，可以根据你的兴趣和需求推荐书籍和文章。

为了给你更好的推荐，我想了解一下：
1. 你平时喜欢阅读什么类型的内容？（如小说、技术、心理学等）
2. 你的阅读水平如何？（初级/中级/高级）
3. 你更喜欢中文还是英文内容？

当然，你也可以直接告诉我你想找什么样的书或文章！"""
        else:
            profile_summary = self.user_profile.get_profile_summary()
            return f"""欢迎回来！ 📚

根据你的阅读偏好：
{profile_summary}

请告诉我你想找什么样的书籍或文章，我会为你推荐最合适的内容！"""
    
    def process_initial_preferences(self, user_input: str):
        """
        处理新用户的初始偏好设置
        
        Args:
            user_input: 用户输入的偏好信息
        """
        # 使用LLM提取偏好信息
        preferences = self.llm_client.extract_preferences_from_conversation(user_input)
        
        # 更新用户画像
        if preferences.get("genres"):
            for genre in preferences["genres"]:
                self.user_profile.add_genre(genre)
        
        if preferences.get("topics"):
            for topic in preferences["topics"]:
                self.user_profile.add_topic(topic)
        
        if preferences.get("authors"):
            for author in preferences["authors"]:
                self.user_profile.add_author(author)
        
        if preferences.get("reading_level"):
            self.user_profile.update_preferences(reading_level=preferences["reading_level"])
    
    def recommend(self, user_input: str, top_k: int = 5) -> Dict:
        """
        根据用户输入生成推荐
        
        Args:
            user_input: 用户输入
            top_k: 返回推荐数量
            
        Returns:
            推荐结果字典
        """
        # 增加交互计数
        self.user_profile.increment_interaction()
        
        # 记录对话历史
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # 如果是新用户的前几次交互，尝试提取偏好信息
        if self.user_profile.is_new_user():
            self.process_initial_preferences(user_input)
        
        # 获取用户画像摘要
        profile_summary = self.user_profile.get_profile_summary()
        
        # 分析用户请求
        request_analysis = self.llm_client.analyze_user_request(user_input, profile_summary)
        
        # 检查是否相关
        if not request_analysis.get("is_related", True):
            return {
                "success": False,
                "is_related": False,
                "message": request_analysis.get("refusal_message", "抱歉，我只能回答与阅读和书籍相关的问题。"),
                "recommendations": []
            }
        
        # 构建搜索查询
        search_query = " ".join(request_analysis.get("topics", []))
        if not search_query:
            search_query = user_input
        
        # 获取候选内容
        content_type = request_analysis.get("content_type", "both")
        language = request_analysis.get("language", "zh")
        
        candidate_items = self.content_fetcher.fetch_content(
            query=search_query,
            content_type=content_type,
            language=language
        )
        
        # 如果没有候选项，返回空结果
        if not candidate_items:
            return {
                "success": False,
                "is_related": True,
                "message": "抱歉，没有找到相关的内容。请尝试换一个关键词或描述。",
                "recommendations": []
            }
        
        # 使用LLM生成推荐
        recommendations = self.llm_client.generate_recommendations(
            user_profile_summary=profile_summary,
            user_request_analysis=request_analysis,
            candidate_items=candidate_items,
            top_k=top_k
        )
        
        # 记录对话历史
        self.conversation_history.append({
            "role": "assistant",
            "content": f"为你推荐了{len(recommendations)}个内容"
        })
        
        return {
            "success": True,
            "message": f"根据你的需求，我为你精心挑选了{len(recommendations)}个推荐：",
            "recommendations": recommendations,
            "request_analysis": request_analysis
        }
    
    def feedback(self, item_id: str, liked: bool, item_info: Optional[Dict] = None):
        """
        接收用户反馈
        
        Args:
            item_id: 推荐项ID
            liked: 是否喜欢
            item_info: 项目信息
        """
        self.user_profile.add_feedback(item_id, liked, item_info)
        
        # 如果用户喜欢，尝试从中提取偏好信息
        if liked and item_info:
            # 可以进一步分析item_info来更新用户偏好
            pass
    
    def format_recommendations(self, result: Dict) -> str:
        """
        格式化推荐结果为可读文本
        
        Args:
            result: 推荐结果字典
            
        Returns:
            格式化的文本
        """
        if not result["success"]:
            return result["message"]
        
        output = [result["message"], ""]
        
        for i, rec in enumerate(result["recommendations"], 1):
            output.append(f"【推荐 {i}】{rec.get('title', 'Unknown')}")
            output.append(f"作者：{rec.get('author', 'Unknown')}")
            output.append(f"来源：{rec.get('source', 'Unknown')}")
            
            if rec.get("description"):
                output.append(f"简介：{rec['description']}")
            
            if rec.get("reason"):
                output.append(f"💡 推荐理由：{rec['reason']}")
            
            if rec.get("highlights"):
                output.append(f"✨ 内容亮点：{rec['highlights']}")
            
            if rec.get("scenario"):
                output.append(f"📖 适合场景：{rec['scenario']}")
            
            if rec.get("url"):
                output.append(f"🔗 链接：{rec['url']}")
            
            if rec.get("score"):
                output.append(f"⭐ 评分：{rec['score']}/10")
            
            output.append("")  # 空行分隔
        
        output.append("---")
        output.append("💬 如果你喜欢某个推荐，请告诉我！这样我能更好地了解你的偏好。")
        
        return "\n".join(output)
    
    def chat(self, user_input: str) -> str:
        """
        主要交互接口
        
        Args:
            user_input: 用户输入
            
        Returns:
            Agent回复
        """
        # 处理特殊命令
        if user_input.lower() in ["exit", "quit", "退出"]:
            return "感谢使用灵魂伴侣推荐系统，期待下次再见！ 👋"
        
        if user_input.lower() in ["help", "帮助"]:
            return """灵魂伴侣推荐系统使用指南：

1. 直接描述你想找的内容，例如：
   - "我想学习机器学习，有什么适合初学者的书？"
   - "推荐一些轻松治愈的小说"
   - "有关于心理学的好文章吗？"

2. 告诉我你的反馈，例如：
   - "我喜欢第一个推荐"
   - "这些太难了，有简单一点的吗？"

3. 更新你的偏好，例如：
   - "我最近对科幻小说感兴趣"
   - "我更喜欢英文内容"

输入 'exit' 或 '退出' 结束对话。"""
        
        # 生成推荐
        result = self.recommend(user_input)
        
        # 格式化输出
        return self.format_recommendations(result)
    
    def run_interactive(self):
        """运行交互式命令行界面"""
        print(self.welcome())
        print("\n" + "="*60 + "\n")
        
        while True:
            try:
                user_input = input("你: ").strip()
                
                if not user_input:
                    continue
                
                response = self.chat(user_input)
                print(f"\n灵魂伴侣: {response}\n")
                print("="*60 + "\n")
                
                if "感谢使用" in response:
                    break
                    
            except KeyboardInterrupt:
                print("\n\n感谢使用灵魂伴侣推荐系统！ 👋")
                break
            except Exception as e:
                print(f"\n发生错误: {str(e)}\n")
