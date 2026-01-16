import { motion } from "framer-motion";
import { ChevronDown, BookMarked, Zap, User } from "lucide-react";
import { useState } from "react";

interface UserProfileSidebarProps {
  userName: string;
  genres: string[];
  topics: string[];
  readingLevel: string;
  interactionCount: number;
  isOpen: boolean;
  onToggle: () => void;
}

export default function UserProfileSidebar({
  userName,
  genres,
  topics,
  readingLevel,
  interactionCount,
  isOpen,
  onToggle,
}: UserProfileSidebarProps) {
  const [expandedSection, setExpandedSection] = useState<string | null>(null);

  const toggleSection = (section: string) => {
    setExpandedSection(expandedSection === section ? null : section);
  };

  return (
    <motion.div
      initial={{ x: 300 }}
      animate={{ x: isOpen ? 0 : 300 }}
      transition={{ duration: 0.3 }}
      className="fixed right-0 top-0 h-screen w-80 bg-card border-l border-border shadow-lg z-40 overflow-y-auto"
    >
      <div className="p-4">
        {/* 关闭按钮 */}
        <button
          onClick={onToggle}
          className="absolute right-4 top-4 p-1 hover:bg-secondary rounded-lg transition-colors"
        >
          <ChevronDown className="w-5 h-5 text-primary rotate-90" />
        </button>

        {/* 用户信息头 */}
        <div className="mt-8 mb-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
              <User className="w-6 h-6 text-primary" />
            </div>
            <div>
              <h3 className="font-semibold text-foreground">{userName}</h3>
              <p className="text-xs text-muted-foreground">
                已交互 {interactionCount} 次
              </p>
            </div>
          </div>
        </div>

        {/* 阅读水平 */}
        <div className="mb-4 p-3 bg-secondary/30 rounded-lg border border-border">
          <div className="flex items-center gap-2 mb-1">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold text-foreground">
              阅读水平
            </span>
          </div>
          <p className="text-sm text-muted-foreground">
            {readingLevel === "beginner"
              ? "初级 - 入门阶段"
              : readingLevel === "intermediate"
                ? "中级 - 有一定基础"
                : "高级 - 深度学习"}
          </p>
        </div>

        {/* 喜欢的类型 */}
        <div className="mb-4">
          <button
            onClick={() => toggleSection("genres")}
            className="w-full flex items-center justify-between p-3 hover:bg-secondary/30 rounded-lg transition-colors"
          >
            <div className="flex items-center gap-2">
              <BookMarked className="w-4 h-4 text-primary" />
              <span className="text-sm font-semibold text-foreground">
                喜欢的类型
              </span>
            </div>
            <ChevronDown
              className={`w-4 h-4 text-muted-foreground transition-transform ${
                expandedSection === "genres" ? "rotate-180" : ""
              }`}
            />
          </button>
          {expandedSection === "genres" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="px-3 pb-3 space-y-2"
            >
              {genres.length > 0 ? (
                genres.map((genre, idx) => (
                  <div
                    key={idx}
                    className="text-sm px-2 py-1 bg-primary/10 text-primary rounded inline-block mr-2 mb-2"
                  >
                    {genre}
                  </div>
                ))
              ) : (
                <p className="text-xs text-muted-foreground">
                  暂无记录，继续交互以发现您的偏好
                </p>
              )}
            </motion.div>
          )}
        </div>

        {/* 感兴趣的主题 */}
        <div className="mb-4">
          <button
            onClick={() => toggleSection("topics")}
            className="w-full flex items-center justify-between p-3 hover:bg-secondary/30 rounded-lg transition-colors"
          >
            <div className="flex items-center gap-2">
              <BookMarked className="w-4 h-4 text-primary" />
              <span className="text-sm font-semibold text-foreground">
                感兴趣的主题
              </span>
            </div>
            <ChevronDown
              className={`w-4 h-4 text-muted-foreground transition-transform ${
                expandedSection === "topics" ? "rotate-180" : ""
              }`}
            />
          </button>
          {expandedSection === "topics" && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="px-3 pb-3 space-y-2"
            >
              {topics.length > 0 ? (
                topics.map((topic, idx) => (
                  <div
                    key={idx}
                    className="text-sm px-2 py-1 bg-accent/10 text-accent rounded inline-block mr-2 mb-2"
                  >
                    {topic}
                  </div>
                ))
              ) : (
                <p className="text-xs text-muted-foreground">
                  暂无记录，继续交互以发现您的偏好
                </p>
              )}
            </motion.div>
          )}
        </div>

        {/* 提示信息 */}
        <div className="mt-6 p-3 bg-secondary/20 rounded-lg border border-border">
          <p className="text-xs text-muted-foreground leading-relaxed">
            💡 您的阅读偏好会随着交互而不断更新，帮助我为您提供更精准的推荐。
          </p>
        </div>
      </div>
    </motion.div>
  );
}
