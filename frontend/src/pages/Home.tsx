import { useState, useRef, useEffect } from "react";
import { motion } from "framer-motion";
import { Send, Menu, BookOpen, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import ChatMessage from "@/components/ChatMessage";
import RecommendationCard from "@/components/RecommendationCard";
import UserProfileSidebar from "@/components/UserProfileSidebar";
import { sendMessage, getUserProfile, submitFeedback } from "@/lib/api";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  isError?: boolean;
  recommendations?: Array<{
    title: string;
    author: string;
    description: string;
    reason: string;
    highlights: string;
    scenario: string;
    score: number;
    url?: string;
    source: string;
  }>;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      role: "assistant",
      content:
        "欢迎来到灵魂伴侣！👋\n\n我是你的个性化阅读推荐助手，专注于为你发现好书和好文章。\n\n请告诉我你想读什么？例如：\n• \"我想学习Python编程\"\n• \"推荐一些轻松治愈的小说\"\n• \"有关于人工智能的最新文章吗？\"\n\n我会根据你的需求为你精心挑选最合适的内容！",
    },
  ]);

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // 用户画像状态
  const [userProfile, setUserProfile] = useState({
    name: "阅读爱好者",
    genres: ["科幻", "文学"],
    topics: ["人工智能", "心理学"],
    readingLevel: "intermediate",
    interactionCount: 2,
  });

  // 自动滚动到底部
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // 发送消息到后端API
  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // 添加用户消息
    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // 调用后端API
      const response = await sendMessage({
        user_id: userProfile.name,
        message: input,
        session_id: Date.now().toString(),
      });

      // 创建助手消息
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message,
        isError: !response.is_related,
        recommendations: response.recommendations,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // 更新用户画像
      try {
        const profile = await getUserProfile(userProfile.name);
        setUserProfile({
          name: profile.user_id,
          genres: profile.preferences.genres || [],
          topics: profile.preferences.topics || [],
          readingLevel: profile.preferences.reading_level || "intermediate",
          interactionCount: profile.interaction_count || 0,
        });
      } catch (error) {
        console.error("获取用户画像失败:", error);
      }

      // 显示成功提示
      if (response.success && response.is_related) {
        toast.success("推荐已生成！");
      } else if (!response.is_related) {
        toast.info("这个问题与阅读无关");
      }
    } catch (error) {
      console.error("发送消息失败:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: `抱歉，发生了错误。请检查后端服务是否正常运行（http://localhost:8010）。\n\n错误信息: ${error instanceof Error ? error.message : "未知错误"}`,
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
      toast.error("发送消息失败，请检查网络连接");
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      {/* 顶部导航栏 */}
      <header className="bg-card border-b border-border px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
            <BookOpen className="w-6 h-6 text-primary" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-foreground">灵魂伴侣</h1>
            <p className="text-xs text-muted-foreground">
              让阅读推荐更懂你
            </p>
          </div>
        </div>

        <Button
          variant="ghost"
          size="icon"
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="relative"
        >
          <Menu className="w-5 h-5" />
        </Button>
      </header>

      {/* 主容器 */}
      <div className="flex-1 flex overflow-hidden">
        {/* 聊天区域 */}
        <div className="flex-1 flex flex-col overflow-hidden">
          {/* 消息列表 */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((message) => (
              <div key={message.id}>
                {/* 文本消息 */}
                <ChatMessage
                  role={message.role}
                  content={message.content}
                  isError={message.isError}
                />

                {/* 推荐卡片 */}
                {message.recommendations && message.recommendations.length > 0 && (
                  <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.4, delay: 0.1 }}
                    className="mt-4 space-y-3"
                  >
                    {message.recommendations.map((rec, idx) => (
                      <RecommendationCard
                        key={idx}
                        {...rec}
                        onLike={async () => {
                          try {
                            await submitFeedback({
                              user_id: userProfile.name,
                              item_id: rec.title,
                              liked: true,
                              item_info: rec,
                            });
                            toast.success("感谢你的反馈！");
                          } catch (error) {
                            toast.error("反馈提交失败");
                          }
                        }}
                        onDislike={async () => {
                          try {
                            await submitFeedback({
                              user_id: userProfile.name,
                              item_id: rec.title,
                              liked: false,
                              item_info: rec,
                            });
                            toast.success("感谢你的反馈！");
                          } catch (error) {
                            toast.error("反馈提交失败");
                          }
                        }}
                      />
                    ))}
                  </motion.div>
                )}
              </div>
            ))}

            {/* 加载指示器 */}
            {isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center gap-2 text-muted-foreground"
              >
                <Loader2 className="w-4 h-4 animate-spin" />
                <span className="text-sm">灵魂伴侣正在思考...</span>
              </motion.div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* 输入框 */}
          <div className="border-t border-border bg-card p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="告诉我你想读什么..."
                disabled={isLoading}
                className="flex-1 px-4 py-2 rounded-lg border border-border bg-input text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary disabled:opacity-50"
              />
              <Button
                onClick={handleSendMessage}
                disabled={isLoading || !input.trim()}
                className="px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground rounded-lg flex items-center gap-2"
              >
                <Send className="w-4 h-4" />
                <span className="hidden sm:inline">发送</span>
              </Button>
            </div>
            <p className="text-xs text-muted-foreground mt-2">
              💡 提示：我专注于阅读推荐，只能回答与书籍、文章相关的问题
            </p>
          </div>
        </div>

        {/* 用户画像侧边栏 */}
        {sidebarOpen && (
          <UserProfileSidebar
            userName={userProfile.name}
            genres={userProfile.genres}
            topics={userProfile.topics}
            readingLevel={userProfile.readingLevel}
            interactionCount={userProfile.interactionCount}
            isOpen={sidebarOpen}
            onToggle={() => setSidebarOpen(false)}
          />
        )}

        {/* 侧边栏遮罩 */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 bg-black/30 z-30"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </div>
  );
}
