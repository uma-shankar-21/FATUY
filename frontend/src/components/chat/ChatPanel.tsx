import {
  useState,
} from "react";

import ChatInput
  from "./chatInput";

import {
  sendChatMessage,
} from "../../api/chat";

import {
  useAuth,
} from "../../context/AuthContext";

import "./ChatPanel.css";


interface Message {

  id: string;

  sender: "AI" | "You";

  content: string;

}


export default function ChatPanel() {

  const [messages, setMessages] =
    useState<Message[]>([
      {
        id: "welcome",

        sender: "AI",

        content:
          "Hello! I’m your banking assistant. Ask me anything about your accounts, transactions, loans or payments.",
      },
    ]);


  // =====================================
  // GET CUSTOMER FROM AUTH CONTEXT
  // =====================================

  const {
    customer,
  } = useAuth();


  const [sessionId, setSessionId] =
    useState<string | null>(null);


  const [loading, setLoading] =
    useState(false);


  async function handleSend(
    message: string
  ) {

    if (loading) {
      return;
    }


    // =====================================
    // GET USER ID
    // =====================================

    const userId =
      customer?.id;


    if (!userId) {

      console.error(
        "USER ID NOT FOUND"
      );

      setMessages(
        (previousMessages) => [
          ...previousMessages,
          {
            id: crypto.randomUUID(),

            sender: "AI",

            content:
              "Unable to identify the current user. Please log in again.",
          },
        ]
      );

      return;
    }


    // =====================================
    // ADD USER MESSAGE IMMEDIATELY
    // =====================================

    const userMessage: Message = {

      id: crypto.randomUUID(),

      sender: "You",

      content: message,

    };


    setMessages(
      (previousMessages) => [
        ...previousMessages,
        userMessage,
      ]
    );


    try {

      setLoading(true);


      // =====================================
      // CALL AI CHAT API
      // =====================================

      const data =
        await sendChatMessage(
          userId,
          message,
          sessionId
        );


      // =====================================
      // SAVE SESSION ID
      // =====================================

      if (data.session_id) {

        setSessionId(
          data.session_id
        );

      }


      // =====================================
      // ADD AI RESPONSE
      // =====================================

      const aiMessage: Message = {

        id: crypto.randomUUID(),

        sender: "AI",

        content: data.response,

      };


      setMessages(
        (previousMessages) => [
          ...previousMessages,
          aiMessage,
        ]
      );

    } catch (error) {

      console.error(
        "CHAT ERROR:",
        error
      );


      setMessages(
        (previousMessages) => [
          ...previousMessages,

          {
            id: crypto.randomUUID(),

            sender: "AI",

            content:
              "Sorry, I couldn't process your request. Please try again.",
          },
        ]
      );

    } finally {

      setLoading(false);

    }

  }


  return (

    <aside className="chat-panel">

      <div className="chat-header">

        <div className="chat-title-row">

          <span className="chat-icon">
            ✦
          </span>

          <h2>
            Banking Assistant
          </h2>

          <span className="online-status">
            Online
          </span>

        </div>

        <p>
          Your AI financial assistant
        </p>

      </div>


      <div className="chat-messages">

        {messages.map(
          (message) => (

            <div
              key={message.id}
              className={
                message.sender === "AI"
                  ? "chat-message assistant-message"
                  : "chat-message user-message"
              }
            >

              <span className="message-sender">

                {message.sender}

              </span>

              <p>

                {message.content}

              </p>

            </div>

          )
        )}


        {loading && (

          <div className="chat-message assistant-message typing-message">

            <span className="message-sender">
              AI
            </span>

            <p>
              Thinking...
            </p>

          </div>

        )}

      </div>


      <ChatInput
        onSend={handleSend}
        loading={loading}
      />

    </aside>

  );

}