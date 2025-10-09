import React, { useState, useRef, useEffect } from "react";
import { Container, Button, Form, Card } from "react-bootstrap";
import "./ChatInterface.css"; // create a separate CSS file for styling

const ChatInterface = ({ onBack }) => {
  const [messages, setMessages] = useState([]); // { sender: "user"|"ai", text: "..." }
  const [input, setInput] = useState("");
  const chatEndRef = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");

    // Call AI backend / OpenAI API here
    // For now, simulate AI response with a delay
    setTimeout(() => {
      const aiMessage = {
        sender: "ai",
        text: `AI Response to: "${userMessage.text}"`,
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <Container className="py-4">
      <Button variant="secondary" onClick={onBack} className="mb-3">
        &larr; Back
      </Button>
      <h4 className="text-light mb-3">AI Chat Assistant</h4>

      <Card className="chat-card mb-3">
        <Card.Body className="chat-body">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${
                msg.sender === "user" ? "user" : "ai"
              }`}
            >
              <strong>{msg.sender === "user" ? "You" : "AI"}:</strong>{" "}
              {msg.text}
            </div>
          ))}
          <div ref={chatEndRef} />
        </Card.Body>
      </Card>

      <Form>
        <div className="d-flex">
          <Form.Control
            type="text"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <Button variant="success" onClick={sendMessage} className="ms-2">
            Send
          </Button>
        </div>
      </Form>
    </Container>
  );
};

export default ChatInterface;
