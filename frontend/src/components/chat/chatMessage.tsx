interface ChatMessageProps {

  role:
    | "user"
    | "assistant";

  content: string;
}


export default function ChatMessage({
  role,
  content,
}: ChatMessageProps) {

  return (

    <div
      className={`chat-message ${role}`}
    >

      {role === "assistant" && (

        <div className="ai-avatar">
          AI
        </div>

      )}


      <div className="message-content">

        {content}

      </div>

    </div>

  );
}