"""
灵魂伴侣 Flask 后端服务器
连接 Python Agent 并提供 REST API
"""

import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from soul_mate import SoulMateAgent

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3008", "http://localhost:3000", "http://127.0.0.1:3008"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# 存储用户 Agent 实例
agents = {}

def get_agent(user_id: str) -> SoulMateAgent:
    """获取或创建用户的 Agent 实例"""
    if user_id not in agents:
        agents[user_id] = SoulMateAgent(user_id=user_id)
    return agents[user_id]


@app.route("/health", methods=["GET"])
def health_check():
    """健康检查端点"""
    return jsonify({"status": "healthy", "service": "soul-mate-agent"}), 200


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    聊天端点
    
    请求体:
    {
        "user_id": "alice",
        "message": "推荐一些关于机器学习的书籍",
        "session_id": "session_123"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "success": False,
                "message": "请求体不能为空"
            }), 400
        
        user_id = data.get("user_id", "default_user")
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify({
                "success": False,
                "message": "消息不能为空"
            }), 400
        
        # 获取用户 Agent
        agent = get_agent(user_id)
        
        # 调用 Agent 的推荐方法
        result = agent.recommend(message, top_k=5)
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"处理请求时出错: {str(e)}"
        }), 500


@app.route("/api/user/<user_id>", methods=["GET"])
def get_user_profile(user_id: str):
    """
    获取用户画像端点
    
    返回:
    {
        "user_id": "alice",
        "preferences": {...},
        "interaction_count": 5,
        "liked_items": [...],
        "disliked_items": [...]
    }
    """
    try:
        agent = get_agent(user_id)
        profile = agent.user_profile.profile
        
        return jsonify({
            "user_id": user_id,
            "preferences": profile["preferences"],
            "interaction_count": profile["interaction_count"],
            "liked_items": profile["feedback"]["liked"][-10:],  # 最近10个
            "disliked_items": profile["feedback"]["disliked"][-10:],
            "created_at": profile["created_at"],
            "updated_at": profile["updated_at"]
        }), 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取用户画像失败: {str(e)}"
        }), 500


@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    """
    提交反馈端点
    
    请求体:
    {
        "user_id": "alice",
        "item_id": "book_123",
        "liked": true,
        "item_info": {
            "title": "机器学习",
            "author": "周志华",
            "type": "book"
        }
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "success": False,
                "message": "请求体不能为空"
            }), 400
        
        user_id = data.get("user_id", "default_user")
        item_id = data.get("item_id")
        liked = data.get("liked", False)
        item_info = data.get("item_info")
        
        if not item_id:
            return jsonify({
                "success": False,
                "message": "item_id 不能为空"
            }), 400
        
        agent = get_agent(user_id)
        agent.feedback(item_id, liked, item_info)
        
        return jsonify({
            "success": True,
            "message": "感谢你的反馈！这将帮助我为你提供更好的推荐。"
        }), 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"提交反馈失败: {str(e)}"
        }), 500


@app.route("/api/users/<user_id>/preferences", methods=["PUT"])
def update_preferences(user_id: str):
    """
    更新用户偏好端点
    
    请求体:
    {
        "genres": ["科幻", "文学"],
        "topics": ["人工智能"],
        "reading_level": "intermediate"
    }
    """
    try:
        data = request.json
        
        if not data:
            return jsonify({
                "success": False,
                "message": "请求体不能为空"
            }), 400
        
        agent = get_agent(user_id)
        
        # 更新偏好
        if "genres" in data:
            for genre in data["genres"]:
                agent.user_profile.add_genre(genre)
        
        if "topics" in data:
            for topic in data["topics"]:
                agent.user_profile.add_topic(topic)
        
        if "reading_level" in data:
            agent.user_profile.update_preferences(reading_level=data["reading_level"])
        
        return jsonify({
            "success": True,
            "message": "偏好已更新",
            "preferences": agent.user_profile.get_preferences()
        }), 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"更新偏好失败: {str(e)}"
        }), 500


@app.route("/api/users/<user_id>/summary", methods=["GET"])
def get_profile_summary(user_id: str):
    """获取用户画像摘要"""
    try:
        agent = get_agent(user_id)
        summary = agent.user_profile.get_profile_summary()
        
        return jsonify({
            "user_id": user_id,
            "summary": summary
        }), 200
        
    except Exception as e:
        print(f"错误: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取摘要失败: {str(e)}"
        }), 500


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({
        "success": False,
        "message": "端点不存在"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """500 错误处理"""
    return jsonify({
        "success": False,
        "message": "服务器内部错误"
    }), 500


if __name__ == "__main__":
    # 检查 OpenAI API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("警告: 未设置 OPENAI_API_KEY 环境变量")
        print("请设置: export OPENAI_API_KEY='your-api-key'")
    
    # 启动服务器
    port = int(os.getenv("FLASK_PORT", 8010))
    debug = os.getenv("FLASK_ENV", "development") == "development"
    
    print(f"启动灵魂伴侣 Flask 服务器...")
    print(f"地址: http://localhost:{port}")
    print(f"调试模式: {debug}")
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        use_reloader=True
    )
