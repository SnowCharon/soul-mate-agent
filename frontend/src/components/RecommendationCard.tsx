import { motion } from "framer-motion";
import { Star, BookOpen, User, ExternalLink, ThumbsUp, ThumbsDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useState } from "react";

interface RecommendationCardProps {
  title: string;
  author: string;
  description: string;
  reason: string;
  highlights: string;
  scenario: string;
  score: number;
  url?: string;
  source: string;
  onLike?: () => void;
  onDislike?: () => void;
}

export default function RecommendationCard({
  title,
  author,
  description,
  reason,
  highlights,
  scenario,
  score,
  url,
  source,
  onLike,
  onDislike,
}: RecommendationCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);
  const [liked, setLiked] = useState<boolean | null>(null);

  const handleLike = () => {
    setLiked(true);
    onLike?.();
  };

  const handleDislike = () => {
    setLiked(false);
    onDislike?.();
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="mb-4"
    >
      <div
        className="bg-gradient-to-br from-white to-secondary/20 border border-border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        {/* 标题和基础信息 */}
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <BookOpen className="w-5 h-5 text-primary flex-shrink-0" />
              <h3 className="text-lg font-semibold text-foreground truncate">
                {title}
              </h3>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground mb-2">
              <User className="w-4 h-4" />
              <span>{author}</span>
              <span className="text-xs bg-secondary/50 px-2 py-1 rounded">
                {source}
              </span>
            </div>
          </div>

          {/* 评分 */}
          <div className="flex items-center gap-1 flex-shrink-0">
            {[...Array(5)].map((_, i) => (
              <Star
                key={i}
                className={`w-4 h-4 ${
                  i < Math.round(score / 2)
                    ? "fill-primary text-primary"
                    : "text-muted"
                }`}
              />
            ))}
            <span className="text-sm font-medium text-primary ml-1">
              {score}/10
            </span>
          </div>
        </div>

        {/* 简介 */}
        <p className="text-sm text-foreground mb-3 line-clamp-2">
          {description}
        </p>

        {/* 展开内容 */}
        {isExpanded && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3 }}
            className="border-t border-border pt-3 mt-3 space-y-3"
          >
            {/* 推荐理由 */}
            <div>
              <h4 className="text-sm font-semibold text-primary mb-1">
                💡 推荐理由
              </h4>
              <p className="text-sm text-foreground">{reason}</p>
            </div>

            {/* 内容亮点 */}
            <div>
              <h4 className="text-sm font-semibold text-primary mb-1">
                ✨ 内容亮点
              </h4>
              <p className="text-sm text-foreground">{highlights}</p>
            </div>

            {/* 适合场景 */}
            <div>
              <h4 className="text-sm font-semibold text-primary mb-1">
                📖 适合场景
              </h4>
              <p className="text-sm text-foreground">{scenario}</p>
            </div>

            {/* 操作按钮 */}
            <div className="flex items-center gap-2 pt-2">
              <Button
                size="sm"
                variant={liked === true ? "default" : "outline"}
                className="flex items-center gap-1"
                onClick={(e) => {
                  e.stopPropagation();
                  handleLike();
                }}
              >
                <ThumbsUp className="w-4 h-4" />
                喜欢
              </Button>
              <Button
                size="sm"
                variant={liked === false ? "destructive" : "outline"}
                className="flex items-center gap-1"
                onClick={(e) => {
                  e.stopPropagation();
                  handleDislike();
                }}
              >
                <ThumbsDown className="w-4 h-4" />
                不喜欢
              </Button>
              {url && (
                <a
                  href={url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ml-auto"
                  onClick={(e) => e.stopPropagation()}
                >
                  <Button size="sm" variant="ghost" className="flex items-center gap-1">
                    <ExternalLink className="w-4 h-4" />
                    查看详情
                  </Button>
                </a>
              )}
            </div>
          </motion.div>
        )}

        {/* 展开提示 */}
        {!isExpanded && (
          <p className="text-xs text-muted-foreground mt-2">
            点击卡片查看详细推荐理由
          </p>
        )}
      </div>
    </motion.div>
  );
}
