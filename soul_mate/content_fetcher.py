"""
内容获取模块
负责从多个来源获取书籍和文章信息
"""

import json
import subprocess
from typing import List, Dict, Optional


class ContentFetcher:
    """内容获取类"""
    
    def __init__(self):
        """初始化内容获取器"""
        pass
    
    def search_huggingface(self, query: str, content_type: str = "dataset") -> List[Dict]:
        """
        通过Hugging Face MCP搜索内容
        
        Args:
            query: 搜索查询
            content_type: 内容类型（dataset, model, paper）
            
        Returns:
            搜索结果列表
        """
        results = []
        
        try:
            # 根据内容类型选择工具
            if content_type == "paper":
                tool_name = "search_papers"
            elif content_type == "model":
                tool_name = "search_models"
            else:
                tool_name = "search_datasets"
            
            # 构建MCP命令
            input_json = json.dumps({"query": query, "limit": 10})
            cmd = [
                "manus-mcp-cli", "tool", "call", tool_name,
                "--server", "hugging-face",
                "--input", input_json
            ]
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # 解析输出
                output = result.stdout
                # MCP输出可能包含多行，尝试解析JSON
                try:
                    data = json.loads(output)
                    if isinstance(data, list):
                        for item in data:
                            results.append({
                                "title": item.get("title") or item.get("name") or item.get("id", "Unknown"),
                                "author": item.get("author", "Unknown"),
                                "description": item.get("description", "No description"),
                                "url": item.get("url", ""),
                                "source": "Hugging Face",
                                "type": content_type
                            })
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            print(f"Hugging Face搜索失败: {str(e)}")
        
        return results
    
    def search_web_articles(self, query: str, language: str = "zh") -> List[Dict]:
        """
        搜索网络文章（模拟实现）
        
        Args:
            query: 搜索查询
            language: 语言偏好
            
        Returns:
            文章列表
        """
        # 这里使用模拟数据，实际应用中可以集成真实的搜索API
        # 或者使用网络爬虫获取文章信息
        
        articles = []
        
        # 模拟一些高质量的文章来源
        if language == "zh":
            sources = [
                {"name": "知乎专栏", "domain": "zhuanlan.zhihu.com"},
                {"name": "少数派", "domain": "sspai.com"},
                {"name": "InfoQ", "domain": "infoq.cn"},
                {"name": "机器之心", "domain": "jiqizhixin.com"},
            ]
        else:
            sources = [
                {"name": "Medium", "domain": "medium.com"},
                {"name": "Towards Data Science", "domain": "towardsdatascience.com"},
                {"name": "ArXiv", "domain": "arxiv.org"},
            ]
        
        # 为每个来源生成模拟文章
        for source in sources[:3]:
            articles.append({
                "title": f"{query}相关文章 - {source['name']}",
                "author": "专栏作者",
                "description": f"这是一篇关于{query}的深度文章，来自{source['name']}。",
                "url": f"https://{source['domain']}/article/example",
                "source": source['name'],
                "type": "article"
            })
        
        return articles
    
    def search_books(self, query: str, language: str = "zh") -> List[Dict]:
        """
        搜索书籍（模拟实现）
        
        Args:
            query: 搜索查询
            language: 语言偏好
            
        Returns:
            书籍列表
        """
        # 这里使用模拟数据，实际应用中可以集成豆瓣API、Google Books API等
        
        books = []
        
        # 根据查询生成模拟书籍数据
        # 实际应用中应该调用真实的书籍数据库API
        
        if "机器学习" in query or "machine learning" in query.lower():
            books.extend([
                {
                    "title": "机器学习",
                    "author": "周志华",
                    "description": "机器学习领域的经典教材，系统全面地介绍了机器学习的基本概念、原理和方法。",
                    "url": "https://book.douban.com/subject/26708119/",
                    "source": "豆瓣读书",
                    "type": "book"
                },
                {
                    "title": "Python机器学习",
                    "author": "Sebastian Raschka",
                    "description": "通过Python实践机器学习，适合初学者入门。",
                    "url": "https://book.douban.com/subject/27000110/",
                    "source": "豆瓣读书",
                    "type": "book"
                },
                {
                    "title": "统计学习方法",
                    "author": "李航",
                    "description": "统计学习方法的经典著作，深入浅出地介绍了各种算法。",
                    "url": "https://book.douban.com/subject/10590856/",
                    "source": "豆瓣读书",
                    "type": "book"
                }
            ])
        
        if "小说" in query or "fiction" in query.lower():
            books.extend([
                {
                    "title": "三体",
                    "author": "刘慈欣",
                    "description": "中国科幻文学的里程碑之作，讲述了人类文明与外星文明的碰撞。",
                    "url": "https://book.douban.com/subject/2567698/",
                    "source": "豆瓣读书",
                    "type": "book"
                },
                {
                    "title": "百年孤独",
                    "author": "加西亚·马尔克斯",
                    "description": "魔幻现实主义的代表作，讲述了布恩迪亚家族七代人的传奇故事。",
                    "url": "https://book.douban.com/subject/6082808/",
                    "source": "豆瓣读书",
                    "type": "book"
                }
            ])
        
        if "心理" in query or "psychology" in query.lower():
            books.extend([
                {
                    "title": "思考，快与慢",
                    "author": "丹尼尔·卡尼曼",
                    "description": "诺贝尔经济学奖得主的经典著作，揭示了人类思维的两种模式。",
                    "url": "https://book.douban.com/subject/10785583/",
                    "source": "豆瓣读书",
                    "type": "book"
                },
                {
                    "title": "心理学与生活",
                    "author": "理查德·格里格",
                    "description": "心理学入门的经典教材，生动有趣地介绍了心理学的各个领域。",
                    "url": "https://book.douban.com/subject/1032501/",
                    "source": "豆瓣读书",
                    "type": "book"
                }
            ])
        
        # 如果没有匹配到特定主题，返回一些通用推荐
        if not books:
            books.extend([
                {
                    "title": f"关于{query}的推荐书籍",
                    "author": "待查询",
                    "description": f"这是一本关于{query}的优质书籍，建议通过豆瓣或其他平台搜索更多信息。",
                    "url": "https://book.douban.com/",
                    "source": "豆瓣读书",
                    "type": "book"
                }
            ])
        
        return books
    
    def fetch_content(
        self, 
        query: str, 
        content_type: str = "both",
        language: str = "zh"
    ) -> List[Dict]:
        """
        综合获取内容
        
        Args:
            query: 搜索查询
            content_type: 内容类型（book, article, both）
            language: 语言偏好
            
        Returns:
            内容列表
        """
        results = []
        
        # 搜索书籍
        if content_type in ["book", "both"]:
            books = self.search_books(query, language)
            results.extend(books)
        
        # 搜索文章
        if content_type in ["article", "both"]:
            articles = self.search_web_articles(query, language)
            results.extend(articles)
        
        # 搜索Hugging Face（主要用于技术/学术内容）
        if any(keyword in query for keyword in ["机器学习", "深度学习", "AI", "数据", "算法"]):
            try:
                hf_papers = self.search_huggingface(query, "paper")
                results.extend(hf_papers[:3])  # 只取前3个
            except:
                pass
        
        return results
