/**
 * 灵魂伴侣 API 客户端
 * 用于与后端 Agent 服务通信
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8010";
const API_TIMEOUT = parseInt(import.meta.env.VITE_API_TIMEOUT || "30000", 10); // 30秒超时

export interface ChatRequest {
  user_id: string;
  message: string;
  session_id: string;
}

export interface Recommendation {
  title: string;
  author: string;
  description: string;
  reason: string;
  highlights: string;
  scenario: string;
  score: number;
  url?: string;
  source: string;
}

export interface ChatResponse {
  success: boolean;
  is_related: boolean;
  message: string;
  recommendations?: Recommendation[];
}

export interface UserProfile {
  user_id: string;
  preferences: {
    genres: string[];
    topics: string[];
    reading_level: string;
    languages: string[];
  };
  interaction_count: number;
  liked_items: any[];
  disliked_items: any[];
}

export interface FeedbackRequest {
  user_id: string;
  item_id: string;
  liked: boolean;
  item_info: any;
}

/**
 * 发送聊天消息
 */
export async function sendMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    const response = await fetch(`${API_BASE_URL}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("请求超时，请检查网络连接");
      }
      throw error;
    }
    throw new Error("发送消息失败");
  }
}

/**
 * 获取用户画像
 */
export async function getUserProfile(userId: string): Promise<UserProfile> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    const response = await fetch(`${API_BASE_URL}/api/user/${userId}`, {
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("请求超时");
      }
      throw error;
    }
    throw new Error("获取用户画像失败");
  }
}

/**
 * 提交反馈
 */
export async function submitFeedback(
  request: FeedbackRequest
): Promise<{ success: boolean; message: string }> {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT);

    const response = await fetch(`${API_BASE_URL}/api/feedback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return await response.json();
  } catch (error) {
    if (error instanceof Error) {
      if (error.name === "AbortError") {
        throw new Error("请求超时");
      }
      throw error;
    }
    throw new Error("提交反馈失败");
  }
}

/**
 * 健康检查
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
      signal: AbortSignal.timeout(5000),
    });
    return response.ok;
  } catch {
    return false;
  }
}
