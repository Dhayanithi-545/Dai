import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import { User, Bot } from "lucide-react";
import WidgetRenderer from "./widgets/WidgetRenderer";
import InsightsPanel from "./widgets/InsightsPanel";

function formatTime() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

const markdownComponents = {
  code({ node, inline, className, children, ...props }) {
    const match = /language-(\w+)/.exec(className || "");
    return !inline && match ? (
      <SyntaxHighlighter
        style={atomDark}
        language={match[1]}
        PreTag="div"
        customStyle={{
          borderRadius: "10px",
          margin: "10px 0",
          fontSize: "13px",
          border: "1px solid var(--border)",
          background: "#0d1117",
        }}
        {...props}
      >
        {String(children).replace(/\n$/, "")}
      </SyntaxHighlighter>
    ) : (
      <code
        style={{
          fontFamily: "var(--font-mono)",
          fontSize: "13px",
          background: "rgba(0,212,255,0.08)",
          border: "1px solid rgba(0,212,255,0.15)",
          borderRadius: "5px",
          padding: "2px 6px",
          color: "#00D4FF",
        }}
        {...props}
      >
        {children}
      </code>
    );
  },
  p({ children }) {
    return <p style={{ margin: "0 0 8px", lineHeight: 1.7 }}>{children}</p>;
  },
  ul({ children }) {
    return <ul style={{ paddingLeft: "18px", margin: "6px 0" }}>{children}</ul>;
  },
  ol({ children }) {
    return <ol style={{ paddingLeft: "18px", margin: "6px 0" }}>{children}</ol>;
  },
  li({ children }) {
    return <li style={{ marginBottom: "3px", lineHeight: 1.65 }}>{children}</li>;
  },
  strong({ children }) {
    return <strong style={{ fontWeight: 600, color: "var(--text-primary)" }}>{children}</strong>;
  },
  table({ children }) {
    return (
      <div style={{ overflowX: "auto", margin: "10px 0" }}>
        <table style={{ borderCollapse: "collapse", width: "100%", fontSize: "13px" }}>
          {children}
        </table>
      </div>
    );
  },
  th({ children }) {
    return (
      <th style={{ padding: "7px 12px", background: "var(--bg-primary)", borderBottom: "1px solid var(--border)", textAlign: "left", fontWeight: 600, color: "var(--text-secondary)" }}>
        {children}
      </th>
    );
  },
  td({ children }) {
    return (
      <td style={{ padding: "7px 12px", borderBottom: "1px solid var(--border)", color: "var(--text-primary)" }}>
        {children}
      </td>
    );
  },
  blockquote({ children }) {
    return (
      <blockquote style={{ borderLeft: "3px solid var(--accent)", margin: "8px 0", paddingLeft: "12px", color: "var(--text-secondary)", fontStyle: "italic" }}>
        {children}
      </blockquote>
    );
  },
};

function MessageBubble({ role, content, widgets, insights, isLast }) {
  const isUser = role === "user";
  const time = formatTime();

  return (
    <div
      style={{
        ...styles.wrapper,
        justifyContent: isUser ? "flex-end" : "flex-start",
        animation: isLast ? "fadeInUp 0.28s ease both" : "none",
      }}
    >
      {/* DAI avatar on the left */}
      {!isUser && (
        <div style={styles.avatarDAI}>
          <Bot size={14} color="#00D4FF" />
        </div>
      )}

      <div style={{ display: "flex", flexDirection: "column", alignItems: isUser ? "flex-end" : "flex-start", maxWidth: isUser ? "70%" : "75%" }}>
        <div
          style={{
            ...(isUser ? styles.userBubble : styles.daiBubble),
          }}
        >
          {isUser ? (
            <span style={styles.userText}>{content}</span>
          ) : (
            <div style={styles.markdownWrapper}>
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={markdownComponents}
              >
                {content}
              </ReactMarkdown>
              <WidgetRenderer widgets={widgets} />
              <InsightsPanel insights={insights} />
            </div>
          )}
        </div>
        <span style={styles.timestamp}>{time}</span>
      </div>

      {/* User avatar on the right */}
      {isUser && (
        <div style={styles.avatarUser}>
          <User size={14} color="var(--text-secondary)" />
        </div>
      )}
    </div>
  );
}

const styles = {
  wrapper: {
    display: "flex",
    alignItems: "flex-end",
    gap: "10px",
    marginBottom: "20px",
  },
  avatarDAI: {
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
  avatarUser: {
    width: "30px",
    height: "30px",
    borderRadius: "50%",
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
  },
  userBubble: {
    background: "var(--accent)",
    color: "#fff",
    borderRadius: "18px 18px 4px 18px",
    padding: "11px 16px",
    fontSize: "15px",
    lineHeight: 1.65,
    wordBreak: "break-word",
  },
  daiBubble: {
    background: "var(--bg-elevated)",
    border: "1px solid var(--border)",
    borderRadius: "18px 18px 18px 4px",
    padding: "14px 18px",
    fontSize: "15px",
    lineHeight: 1.7,
    color: "var(--text-primary)",
    wordBreak: "break-word",
  },
  userText: {
    fontFamily: "var(--font-body)",
    fontWeight: 500,
    color:"black",
  },
  markdownWrapper: {
    fontFamily: "var(--font-body)",
  },
  timestamp: {
    fontSize: "11px",
    color: "var(--text-muted)",
    marginTop: "5px",
    fontFamily: "var(--font-mono)",
  },
};

export default MessageBubble;
