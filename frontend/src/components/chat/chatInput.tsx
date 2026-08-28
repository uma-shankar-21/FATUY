import {
  useState,
} from "react";


interface ChatInputProps {

  onSend: (
    message: string
  ) => void;

  loading: boolean;

}


export default function ChatInput({
  onSend,
  loading,
}: ChatInputProps) {

  const [
    message,
    setMessage,
  ] = useState("");


  function handleSubmit(
    event: React.FormEvent
  ) {

    event.preventDefault();


    const trimmedMessage =
      message.trim();


    if (
      !trimmedMessage ||
      loading
    ) {
      return;
    }


    onSend(
      trimmedMessage
    );


    setMessage("");

  }


  return (

    <form
      className="chat-input-container"
      onSubmit={handleSubmit}
    >

      <input
        className="chat-input"
        type="text"
        placeholder="Ask about your accounts..."
        value={message}
        disabled={loading}
        onChange={(event) =>
          setMessage(
            event.target.value
          )
        }
      />


      <button
        className="chat-send-button"
        type="submit"
        disabled={loading}
      >

        {loading
          ? "..."
          : "Send"}

      </button>

    </form>

  );

}