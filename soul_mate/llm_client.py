"""
LLM客户端模块
负责与大语言模型的交互（支持OpenAI兼容的API）
"""

import os
import json
from openai import OpenAI
from typing import List, Dict, Optional


class LLMClient:
    """LLM客户端类 - 支持OpenAI兼容的API（如HaiHub的Kimi模型）"""
    
    def __init__(self, model: Optional[str] = None, api_key: Optional[str] = None, api_base: Optional[str] = None):
        """
        初始化LLM客户端
        
        Args:
            model: 使用的模型名称（默认从环境变量读取）
            api_key: API密钥（默认从环境变量读取）
            api_base: API基础URL（默认从环境变量读取）
        """
        # 从环境变量读取配置
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_base = api_base or os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4-mini")
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY 环境变量未设置")
        
        # 初始化OpenAI客户端（兼容HaiHub等API）
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.api_base
        )
        
        print(f"✓ LLM客户端已初始化")
        print(f"  模型: {self.model}")
        print(f"  API端点: {self.api_base}")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度参数
            
        Returns:
            模型回复内容
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"LLM调用失败: {str(e)}"
            print(f"❌ {error_msg}")
            return error_msg
    
    def analyze_user_request(self, user_input: str, user_profile_summary: str) -> Dict:
        """
        分析用户请求，提取关键信息
        
        Args:
            user_input: 用户输入
            user_profile_summary: 用户画像摘要
            
        Returns:
            分析结果字典
        """
        system_prompt = """你是一个名为"灵魂伴侣"的专业阅读推荐Agent。你的核心职责是根据用户的需求和喜好推荐好书和好文章。

你的角色属性：
1. 专注性：你只回答与书籍、文章、阅读、文学、学术资料和知识探索相关的问题。
2. 引导性：如果用户的问题与阅读无关，你应该礼貌地拒绝，并引导用户回到阅读话题上。
3. 深度：你对书籍和文章有深刻的见解，推荐理由应体现出对内容的理解。

任务：
请分析用户的需求，首先判断该需求是否与阅读/书籍/文章相关。
如果相关，提取以下信息并返回JSON。
如果不相关，请在JSON中将 "is_related" 设为 false，并提供一段礼貌的拒绝话术。

返回JSON格式：
{
  "is_related": true,
  "topics": ["关键词"],
  "content_type": "book/article/both",
  "purpose": "learning/entertainment/etc",
  "level": "beginner/intermediate/advanced",
  "mood": "情感倾向",
  "language": "zh/en",
  "refusal_message": null
}

如果不相关：
{
  "is_related": false,
  "refusal_message": "抱歉，作为您的'灵魂伴侣'阅读助手，我专注于为您发现好书和好文章。关于[用户话题]的问题，我可能无法为您提供专业的建议。不如我们聊聊您最近想读什么类型的书？"
}"""
        
        user_message = f"""用户画像：
{user_profile_summary}

用户请求：
{user_input}

请分析并返回JSON格式的结果。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat(messages, temperature=0.3)
        
        # 尝试解析JSON
        try:
            # 提取JSON部分（可能包含在markdown代码块中）
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"⚠️  JSON解析失败: {e}")
            # 解析失败，返回默认值
            return {
                "is_related": True,
                "topics": [],
                "content_type": "book",
                "purpose": "general",
                "level": "intermediate",
                "mood": "neutral",
                "language": "zh",
                "refusal_message": None
            }
    
    def generate_recommendations(
        self, 
        user_profile_summary: str,
        user_request_analysis: Dict,
        candidate_items: List[Dict],
        top_k: int = 5
    ) -> List[Dict]:
        """
        基于候选项生成推荐结果
        
        Args:
            user_profile_summary: 用户画像摘要
            user_request_analysis: 用户请求分析结果
            candidate_items: 候选项列表
            top_k: 返回前k个推荐
            
        Returns:
            推荐结果列表
        """
        if not candidate_items:
            return []
        
        # 构建候选项描述
        candidates_text = "\n\n".join([
            f"[{i+1}] 标题: {item.get('title', 'Unknown')}\n"
            f"作者: {item.get('author', 'Unknown')}\n"
            f"描述: {item.get('description', 'No description')}\n"
            f"来源: {item.get('source', 'Unknown')}"
            for i, item in enumerate(candidate_items[:20])  # 最多处理20个候选项
        ])
        
        system_prompt = f"""你是一个专业的阅读推荐专家。请根据用户画像和需求，从候选项中选择最合适的{top_k}个推荐。

对每个推荐，请提供：
1. 推荐理由（为什么适合这个用户）
2. 内容亮点（这本书/文章的特色）
3. 适合场景（什么时候读）
4. 评分（1-10分）

请以JSON数组格式返回，每个推荐包含：
- index: 候选项序号（从1开始）
- title: 标题
- reason: 推荐理由
- highlights: 内容亮点
- scenario: 适合场景
- score: 评分（1-10）

例如：
[
  {{
    "index": 1,
    "title": "书名",
    "reason": "推荐理由...",
    "highlights": "内容亮点...",
    "scenario": "适合场景...",
    "score": 9
  }}
]"""
        
        user_message = f"""用户画像：
{user_profile_summary}

用户需求分析：
{user_request_analysis}

候选项列表：
{candidates_text}

请选择最合适的{top_k}个推荐并返回JSON格式结果。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        response = self.chat(messages, temperature=0.5)
        
        # 解析JSON
        try:
            # 提取JSON部分
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            recommendations = json.loads(json_str)
            
            # 合并候选项信息和推荐信息
            result = []
            for rec in recommendations[:top_k]:
                idx = rec.get("index", 1) - 1
                if 0 <= idx < len(candidate_items):
                    item = candidate_items[idx].copy()
                    item.update({
                        "reason": rec.get("reason", ""),
                        "highlights": rec.get("highlights", ""),
                        "scenario": rec.get("scenario", ""),
                        "score": rec.get("score", 7)
                    })
                    result.append(item)
            
            return result
        except Exception as e:
            print(f"⚠️  推荐JSON解析失败: {e}")
            # 解析失败，返回前top_k个候选项
            return candidate_items[:top_k]
    
    def extract_preferences_from_conversation(self, conversation_history: str) -> Dict:
        """
        从对话历史中提取用户偏好
        
        Args:
            conversation_history: 对话历史
            
        Returns:
            提取的偏好信息
        """
        system_prompt = """分析对话历史，提取用户的阅读偏好信息。

请提取：
1. genres: 喜欢的类型列表
2. topics: 感兴趣的主题列表
3. authors: 喜欢的作者列表
4. reading_level: 阅读水平（beginner/intermediate/advanced）

返回JSON格式：
{
  "genres": ["科幻", "推理"],
  "topics": ["人工智能", "心理学"],
  "authors": ["刘慈欣"],
  "reading_level": "intermediate"
}"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"对话历史：\n{conversation_history}"}
        ]
        
        response = self.chat(messages, temperature=0.3)
        
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
            else:
                json_str = response.strip()
            
            return json.loads(json_str)
        except Exception as e:
            print(f"⚠️  偏好提取失败: {e}")
            return {
                "genres": [],
                "topics": [],
                "authors": [],
                "reading_level": "intermediate"
            }
