import { motion } from "framer-motion";
import { BookOpen, AlertCircle } from "lucide-react";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  isError?: boolean;
}

export default function ChatMessage({
  role,
  content,
  isError = false,
}: ChatMessageProps) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}
    >
      <div
        className={`max-w-2xl px-4 py-3 rounded-lg ${
          isUser
            ? "bg-primary text-primary-foreground rounded-br-none"
            : isError
              ? "bg-destructive/10 text-destructive border border-destructive/30 rounded-bl-none"
              : "bg-card text-card-foreground border border-border rounded-bl-none"
        }`}
      >
        <div className="flex items-start gap-2">
          {!isUser && !isError && (
            <BookOpen className="w-5 h-5 text-primary mt-0.5 flex-shrink-0" />
          )}
          {!isUser && isError && (
            <AlertCircle className="w-5 h-5 text-destructive mt-0.5 flex-shrink-0" />
          )}
          <p className="text-sm leading-relaxed whitespace-pre-wrap">{content}</p>
        </div>
      </div>
    </motion.div>
  );
}
