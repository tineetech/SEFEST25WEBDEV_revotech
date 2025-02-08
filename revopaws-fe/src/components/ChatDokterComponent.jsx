import React, { useState, useEffect } from "react";
import { db } from "../utils/firebaseConfig";
import { ref, push, onValue } from "firebase/database";

const ChatDokterCompomemt = () => {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");

  useEffect(() => {
    const messagesRef = ref(db, "chats");
    onValue(messagesRef, (snapshot) => {
      const data = snapshot.val();
      if (data) {
        setMessages(Object.values(data));
      }
    });
  }, []);

  const sendMessage = () => {
    if (text.trim()) {
      push(ref(db, "chats"), {
        text,
        timestamp: Date.now(),
      });
      setText("");
    }
  };

  return (
    <div className="bg-gray-700 p-3 rounded-sm w-80 h-80">
      <div>
        {messages.map((msg, index) => (
          <p key={index}>{msg.text}</p>
        ))}
      </div>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Ketik pesan..."
      />
      <button onClick={sendMessage}>Kirim</button>
    </div>
  );
};

export default ChatDokterCompomemt;
