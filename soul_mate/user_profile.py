"""
用户画像管理模块
负责用户偏好的存储、更新和查询
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class UserProfile:
    """用户画像类"""
    
    def __init__(self, user_id: str, data_dir: str = "data/user_profiles"):
        """
        初始化用户画像
        
        Args:
            user_id: 用户唯一标识
            data_dir: 用户数据存储目录
        """
        self.user_id = user_id
        self.data_dir = data_dir
        self.profile_path = os.path.join(data_dir, f"{user_id}.json")
        
        # 确保数据目录存在
        os.makedirs(data_dir, exist_ok=True)
        
        # 加载或初始化用户画像
        self.profile = self._load_profile()
    
    def _load_profile(self) -> Dict:
        """加载用户画像数据"""
        if os.path.exists(self.profile_path):
            with open(self.profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 初始化默认画像
            return {
                "user_id": self.user_id,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "preferences": {
                    "genres": [],  # 喜欢的类型
                    "topics": [],  # 感兴趣的主题
                    "authors": [],  # 喜欢的作者
                    "reading_level": "intermediate",  # 阅读水平: beginner, intermediate, advanced
                    "content_types": ["book", "article"],  # 内容类型偏好
                    "languages": ["zh", "en"],  # 语言偏好
                },
                "reading_history": [],  # 阅读历史
                "feedback": {
                    "liked": [],  # 喜欢的推荐
                    "disliked": [],  # 不喜欢的推荐
                },
                "interaction_count": 0,  # 交互次数
            }
    
    def save(self):
        """保存用户画像到文件"""
        self.profile["updated_at"] = datetime.now().isoformat()
        with open(self.profile_path, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)
    
    def update_preferences(self, **kwargs):
        """
        更新用户偏好
        
        Args:
            **kwargs: 偏好字段和值
        """
        for key, value in kwargs.items():
            if key in self.profile["preferences"]:
                self.profile["preferences"][key] = value
        self.save()
    
    def add_genre(self, genre: str):
        """添加喜欢的类型"""
        if genre not in self.profile["preferences"]["genres"]:
            self.profile["preferences"]["genres"].append(genre)
            self.save()
    
    def add_topic(self, topic: str):
        """添加感兴趣的主题"""
        if topic not in self.profile["preferences"]["topics"]:
            self.profile["preferences"]["topics"].append(topic)
            self.save()
    
    def add_author(self, author: str):
        """添加喜欢的作者"""
        if author not in self.profile["preferences"]["authors"]:
            self.profile["preferences"]["authors"].append(author)
            self.save()
    
    def add_reading_history(self, item: Dict):
        """
        添加阅读历史
        
        Args:
            item: 阅读记录，包含title, type, timestamp等信息
        """
        item["timestamp"] = datetime.now().isoformat()
        self.profile["reading_history"].append(item)
        self.save()
    
    def add_feedback(self, item_id: str, liked: bool, item_info: Optional[Dict] = None):
        """
        添加用户反馈
        
        Args:
            item_id: 推荐项目ID
            liked: 是否喜欢
            item_info: 项目详细信息
        """
        feedback_entry = {
            "item_id": item_id,
            "timestamp": datetime.now().isoformat(),
        }
        if item_info:
            feedback_entry.update(item_info)
        
        if liked:
            self.profile["feedback"]["liked"].append(feedback_entry)
            # 从不喜欢列表中移除（如果存在）
            self.profile["feedback"]["disliked"] = [
                f for f in self.profile["feedback"]["disliked"] 
                if f.get("item_id") != item_id
            ]
        else:
            self.profile["feedback"]["disliked"].append(feedback_entry)
            # 从喜欢列表中移除（如果存在）
            self.profile["feedback"]["liked"] = [
                f for f in self.profile["feedback"]["liked"] 
                if f.get("item_id") != item_id
            ]
        
        self.save()
    
    def increment_interaction(self):
        """增加交互计数"""
        self.profile["interaction_count"] += 1
        self.save()
    
    def get_preferences(self) -> Dict:
        """获取用户偏好"""
        return self.profile["preferences"]
    
    def get_reading_history(self) -> List[Dict]:
        """获取阅读历史"""
        return self.profile["reading_history"]
    
    def get_liked_items(self) -> List[Dict]:
        """获取喜欢的项目"""
        return self.profile["feedback"]["liked"]
    
    def get_disliked_items(self) -> List[Dict]:
        """获取不喜欢的项目"""
        return self.profile["feedback"]["disliked"]
    
    def is_new_user(self) -> bool:
        """判断是否为新用户（交互次数少于3次）"""
        return self.profile["interaction_count"] < 3
    
    def get_profile_summary(self) -> str:
        """获取用户画像摘要（用于LLM理解）"""
        prefs = self.profile["preferences"]
        summary_parts = []
        
        if prefs["genres"]:
            summary_parts.append(f"喜欢的类型: {', '.join(prefs['genres'])}")
        
        if prefs["topics"]:
            summary_parts.append(f"感兴趣的主题: {', '.join(prefs['topics'])}")
        
        if prefs["authors"]:
            summary_parts.append(f"喜欢的作者: {', '.join(prefs['authors'])}")
        
        summary_parts.append(f"阅读水平: {prefs['reading_level']}")
        
        if self.profile["feedback"]["liked"]:
            liked_titles = [item.get("title", "") for item in self.profile["feedback"]["liked"][-5:]]
            summary_parts.append(f"最近喜欢的内容: {', '.join(liked_titles)}")
        
        return "\n".join(summary_parts) if summary_parts else "新用户，暂无偏好信息"
