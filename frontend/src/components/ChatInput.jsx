import { useState, useRef, useEffect } from "react";
import { SendHorizontal } from "lucide-react";

function ChatInput({ onSend, loading }) {
  const [message, setMessage] = useState("");
  const [focused, setFocused] = useState(false);
  const textareaRef = useRef(null);

  // Auto-grow textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 160) + "px";
  }, [message]);

  const handleSend = () => {
    if (!message.trim() || loading) return;
    onSend(message);
    setMessage("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
    // Ctrl+Enter also sends
    if (e.key === "Enter" && e.ctrlKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend = message.trim().length > 0 && !loading;

  return (
    <div style={styles.wrapper}>
      <div
        style={{
          ...styles.inputBox,
          borderColor: focused ? "rgba(0,212,255,0.5)" : "var(--border)",
          boxShadow: focused ? "0 0 0 3px rgba(0,212,255,0.07)" : "none",
        }}
      >
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          placeholder="Ask DAI about vehicles, reports, or manufacturing data..."
          rows={1}
          style={styles.textarea}
          disabled={loading}
        />
        <button
          onClick={handleSend}
          disabled={!canSend}
          style={{
            ...styles.sendBtn,
            background: canSend ? "var(--accent)" : "var(--bg-elevated)",
            color: canSend ? "#000" : "var(--text-muted)",
            cursor: canSend ? "pointer" : "not-allowed",
            boxShadow: canSend ? "0 0 12px rgba(0,212,255,0.3)" : "none",
          }}
          title="Send message"
        >
          <SendHorizontal size={17} />
        </button>
      </div>
      <p style={styles.hint}>
        Press <kbd style={styles.kbd}>Enter</kbd> to send · <kbd style={styles.kbd}>Shift+Enter</kbd> for new line
      </p>
    </div>
  );
}

const styles = {
  wrapper: {
    padding: "14px 32px 20px",
    borderTop: "1px solid var(--border)",
    background: "var(--bg-secondary)",
    flexShrink: 0,
  },
  inputBox: {
    display: "flex",
    alignItems: "flex-end",
    gap: "10px",
    background: "var(--bg-elevated)",
    border: "1px solid",
    borderRadius: "16px",
    padding: "10px 12px 10px 16px",
    transition: "border-color 0.2s, box-shadow 0.2s",
  },
  textarea: {
    flex: 1,
    background: "transparent",
    border: "none",
    outline: "none",
    resize: "none",
    color: "var(--text-primary)",
    fontSize: "15px",
    fontFamily: "var(--font-body)",
    lineHeight: 1.6,
    minHeight: "24px",
    maxHeight: "160px",
    overflowY: "auto",
  },
  sendBtn: {
    width: "36px",
    height: "36px",
    borderRadius: "10px",
    border: "none",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    transition: "background 0.2s, box-shadow 0.2s, transform 0.15s",
    alignSelf: "flex-end",
  },
  hint: {
    fontSize: "11px",
    color: "var(--text-muted)",
    marginTop: "8px",
    textAlign: "center",
    fontFamily: "var(--font-mono)",
  },
  kbd: {
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "4px",
    padding: "1px 5px",
    fontSize: "10px",
    color: "var(--text-secondary)",
  },
};

export default ChatInput;
