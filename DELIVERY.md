# 灵魂伴侣 Agent - 项目交付文档

## 📦 项目概述

**项目名称**: 灵魂伴侣 (Soul Mate Agent)  
**GitHub仓库**: https://github.com/SnowCharon/soul-mate-agent  
**创建时间**: 2026-01-16  

这是一个基于大语言模型的个性化阅读推荐Agent，能够根据用户的个人需求和喜好智能推荐书籍和文章。

## ✨ 核心功能

### 1. 用户画像管理
- **动态偏好学习**: 自动从对话中提取用户的阅读偏好
- **持久化存储**: 用户画像以JSON格式保存，支持多用户
- **偏好维度**: 类型、主题、作者、阅读水平、语言偏好等
- **反馈机制**: 记录用户的喜欢/不喜欢，持续优化推荐

### 2. 智能推荐引擎
- **需求分析**: 使用LLM深度理解用户的自然语言描述
- **多维度推荐**: 基于内容、用户画像和情境的综合推荐
- **详细理由**: 为每个推荐提供推荐理由、内容亮点、适用场景
- **评分系统**: 对推荐项目进行1-10分的质量评分

### 3. 多源内容集成
- **书籍数据库**: 集成豆瓣等书籍信息源
- **网络文章**: 搜索知乎、Medium等优质文章平台
- **学术资源**: 通过Hugging Face MCP搜索论文和数据集
- **可扩展**: 易于添加新的内容源

### 4. 自然语言交互
- **对话式界面**: 支持自然语言对话，无需复杂命令
- **上下文理解**: 记录对话历史，理解多轮对话上下文
- **友好提示**: 为新用户提供引导和帮助信息

## 🏗️ 技术架构

### 模块设计

```
soul_mate/
├── agent.py           # Agent主类 - 整合所有模块
├── user_profile.py    # 用户画像管理 - 偏好存储和更新
├── llm_client.py      # LLM客户端 - 与GPT模型交互
└── content_fetcher.py # 内容获取 - 多源内容搜索
```

### 技术栈
- **Python 3.11+**: 核心开发语言
- **OpenAI API**: 使用GPT-4.1-mini模型进行智能分析
- **Hugging Face MCP**: 学术内容搜索集成
- **JSON**: 轻量级数据持久化

### 设计特点
- **模块化**: 各模块职责清晰，易于维护和扩展
- **可配置**: 支持自定义用户ID、模型选择等
- **可扩展**: 易于添加新的内容源和推荐策略
- **用户友好**: 提供命令行交互和程序化API两种使用方式

## 🚀 使用方式

### 方式一：命令行交互

```bash
# 克隆仓库
git clone https://github.com/SnowCharon/soul-mate-agent.git
cd soul-mate-agent

# 安装依赖
pip install -r requirements.txt

# 设置API密钥
export OPENAI_API_KEY='your-api-key'

# 运行Agent
python main.py
```

### 方式二：程序化调用

```python
from soul_mate import SoulMateAgent

# 创建Agent实例
agent = SoulMateAgent(user_id="alice", model="gpt-4.1-mini")

# 获取推荐
result = agent.recommend("推荐一些关于机器学习的书籍", top_k=5)

# 处理结果
if result["success"]:
    for rec in result["recommendations"]:
        print(f"{rec['title']} - {rec['author']}")
        print(f"推荐理由: {rec['reason']}")
```

### 方式三：运行示例

```bash
# 运行完整的示例程序
python examples/demo.py
```

## 📊 项目文件说明

| 文件/目录 | 说明 |
|----------|------|
| `main.py` | 主程序入口，提供命令行交互界面 |
| `soul_mate/` | 核心模块目录 |
| `soul_mate/agent.py` | Agent主类，整合所有功能 |
| `soul_mate/user_profile.py` | 用户画像管理模块 |
| `soul_mate/llm_client.py` | LLM客户端，处理与GPT的交互 |
| `soul_mate/content_fetcher.py` | 内容获取模块，支持多源搜索 |
| `examples/demo.py` | 使用示例和演示代码 |
| `data/user_profiles/` | 用户画像数据存储目录 |
| `tests/` | 测试代码目录 |
| `README.md` | 项目说明文档 |
| `design.md` | 详细设计文档 |
| `requirements.txt` | Python依赖列表 |
| `LICENSE` | MIT开源协议 |

## 🎯 使用场景

### 1. 专业学习
```
用户: "我想深入学习深度学习，需要一些进阶的书籍"
Agent: 分析需求 → 推荐《深度学习》(Goodfellow)等专业书籍
```

### 2. 休闲阅读
```
用户: "最近工作压力大，想看一些轻松治愈的小说"
Agent: 理解情感需求 → 推荐治愈系文学作品
```

### 3. 探索新领域
```
用户: "我对量子计算感兴趣，但完全不了解，有什么入门文章吗？"
Agent: 搜索入门内容 → 推荐适合初学者的文章和书籍
```

### 4. 主题研究
```
用户: "我在研究人工智能伦理，需要相关的论文和文章"
Agent: 搜索学术资源 → 推荐相关论文和深度文章
```

## 🔧 扩展指南

### 添加新的内容源

在 `content_fetcher.py` 中添加新的搜索方法：

```python
def search_custom_source(self, query: str) -> List[Dict]:
    """搜索自定义内容源"""
    # 实现搜索逻辑
    results = []
    # ... 获取内容
    return results
```

### 自定义推荐策略

在 `llm_client.py` 中修改提示词和推荐逻辑：

```python
def generate_recommendations(self, ...):
    # 自定义system_prompt
    system_prompt = "你是一个专业的推荐专家..."
    # ... 实现自定义逻辑
```

### 添加新的用户偏好维度

在 `user_profile.py` 中扩展用户画像结构：

```python
"preferences": {
    "genres": [],
    "topics": [],
    "custom_field": [],  # 添加新字段
    # ...
}
```

## 📈 未来改进方向

1. **内容源扩展**
   - 集成更多书籍API（Google Books、Open Library）
   - 添加视频课程推荐（YouTube、Coursera）
   - 集成播客和音频内容

2. **推荐算法优化**
   - 实现协同过滤算法
   - 添加基于深度学习的推荐模型
   - 引入A/B测试框架

3. **用户体验提升**
   - 开发Web界面
   - 添加移动端支持
   - 实现推荐结果的可视化展示

4. **社交功能**
   - 用户之间的推荐分享
   - 阅读小组和讨论功能
   - 好友推荐系统

5. **数据分析**
   - 用户行为分析仪表板
   - 推荐效果评估指标
   - 内容流行度趋势分析

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📝 开发日志

### v1.0.0 (2026-01-16)
- ✅ 实现用户画像管理模块
- ✅ 实现LLM客户端集成
- ✅ 实现多源内容获取
- ✅ 实现Agent主类和交互界面
- ✅ 添加完整的文档和示例
- ✅ 发布到GitHub

## 📞 联系方式

- GitHub仓库: https://github.com/SnowCharon/soul-mate-agent
- 问题反馈: https://github.com/SnowCharon/soul-mate-agent/issues

## 📄 许可证

本项目采用MIT许可证 - 详见 [LICENSE](LICENSE) 文件

---

**灵魂伴侣** - 让阅读推荐更懂你 ❤️
