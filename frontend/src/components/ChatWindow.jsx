import { useEffect, useRef, useState } from "react";
import MessageBubble from "./MessageBubble";
import { ArrowDown } from "lucide-react";

function TypingIndicator() {
  return (
    <div style={styles.typingWrapper}>
      <div style={styles.typingAvatar}>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </div>
      <div style={styles.typingBubble}>
        <span style={{ ...styles.dot, animationDelay: "0ms" }} />
        <span style={{ ...styles.dot, animationDelay: "160ms" }} />
        <span style={{ ...styles.dot, animationDelay: "320ms" }} />
      </div>
    </div>
  );
}

function EmptyState() {
  return (
    <div style={styles.emptyState}>
      <div style={styles.emptyIcon}>
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#00D4FF" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
          <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
          <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
        </svg>
      </div>
      <p style={styles.emptyTitle}>Ask DAI anything</p>
      <p style={styles.emptySubtitle}>Vehicle details · Manufacturing reports · Dhaya Electric data</p>
    </div>
  );
}

function ChatWindow({ messages, loading }) {
  const bottomRef = useRef(null);
  const containerRef = useRef(null);
  const [showScrollBtn, setShowScrollBtn] = useState(false);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleScroll = () => {
    const el = containerRef.current;
    if (!el) return;
    const isNearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 120;
    setShowScrollBtn(!isNearBottom);
  };

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div style={styles.outer}>
      <div
        ref={containerRef}
        style={styles.container}
        onScroll={handleScroll}
      >
        {messages.length === 0 && !loading ? (
          <EmptyState />
        ) : (
          <>
            {messages.map((message, index) => (
              <MessageBubble
                key={index}
                role={message.role}
                content={message.content}
                widgets={message.widgets}
                insights={message.insights}
                isLast={index === messages.length - 1}
              />
            ))}
            {loading && <TypingIndicator />}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {showScrollBtn && (
        <button
          onClick={scrollToBottom}
          style={styles.scrollBtn}
          title="Scroll to bottom"
        >
          <ArrowDown size={15} />
        </button>
      )}
    </div>
  );
}

const styles = {
  outer: {
    flex: 1,
    position: "relative",
    overflow: "hidden",
  },
  container: {
    height: "100%",
    overflowY: "auto",
    padding: "28px 32px 16px",
    display: "flex",
    flexDirection: "column",
    gap: "4px",
  },
  emptyState: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    gap: "12px",
    margin: "auto",
    paddingTop: "80px",
    opacity: 0.6,
  },
  emptyIcon: {
    width: "56px",
    height: "56px",
    borderRadius: "16px",
    background: "var(--accent-muted)",
    border: "1px solid rgba(0,212,255,0.2)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: "4px",
  },
  emptyTitle: {
    fontFamily: "var(--font-display)",
    fontSize: "16px",
    fontWeight: 600,
    color: "var(--text-primary)",
  },
  emptySubtitle: {
    fontSize: "13px",
    color: "var(--text-muted)",
    textAlign: "center",
    lineHeight: 1.6,
  },
  typingWrapper: {
    display: "flex",
    alignItems: "flex-end",
    gap: "10px",
    padding: "4px 0 8px",
    animation: "fadeInUp 0.25s ease both",
  },
  typingAvatar: {
    width: "30px",
    height: "30px",
    borderRadius: "50%",
    background: "var(--accent-muted)",
    border: "1px solid rgba(0,212,255,0.25)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  typingBubble: {
    display: "flex",
    alignItems: "center",
    gap: "5px",
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "18px 18px 18px 4px",
    padding: "11px 16px",
  },
  dot: {
    display: "inline-block",
    width: "6px",
    height: "6px",
    borderRadius: "50%",
    background: "var(--accent)",
    animation: "dotBounce 1.2s ease-in-out infinite",
  },
  scrollBtn: {
    position: "absolute",
    bottom: "16px",
    left: "50%",
    transform: "translateX(-50%)",
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "50%",
    width: "34px",
    height: "34px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    cursor: "pointer",
    color: "var(--text-secondary)",
    animation: "fadeIn 0.2s ease both",
    boxShadow: "0 4px 16px rgba(0,0,0,0.4)",
    transition: "border-color 0.2s, color 0.2s",
  },
};

export default ChatWindow;
