import apiClient from "./client";

interface ChatRequest {
  user_id: string;

  message: string;

  provider: string;

  session_id?: string;
}

export async function sendChatMessage(
  userId: string,
  message: string,
  sessionId: string | null,
) {
  const payload: ChatRequest = {
    user_id: userId,

    message: message,

    provider: "ollama",
  };

  // Only from the SECOND message onwards
  if (sessionId) {
    payload.session_id = sessionId;
  }

  console.log("AI CHAT PAYLOAD:", payload);

  const response = await apiClient.post("/ai/chat", payload);

  console.log("AI CHAT RESPONSE:", response.data);

  return response.data;
}
