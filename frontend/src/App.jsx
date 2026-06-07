import { useState } from "react";
import "./index.css";
import "./App.css";
import LandingPage from "./pages/LandingPage";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import TracePanel from "./components/TracePanel";
import { sendMessage } from "./services/api";
import { Zap, SquarePen, ArrowLeft } from "lucide-react";

function ChatPage({ initialQuery, onBack }) {
  // ── All original state variables preserved ──
  const [messages, setMessages] = useState([]);
  const [trace, setTrace] = useState([]);
  const [loading, setLoading] = useState(false);
  const [bootstrapped, setBootstrapped] = useState(false);

  // ── Original handleSend logic preserved exactly ──
  const handleSend = async (message) => {
    const userMessage = { role: "user", content: message };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);

    try {
      const data = await sendMessage(message);
      setTrace(data.trace || []);
      const botMessage = { role: "assistant", content: data.response };
      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Backend connection failed." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Fire initial query from landing page hero input (once)
  if (initialQuery && !bootstrapped) {
    setBootstrapped(true);
    setTimeout(() => handleSend(initialQuery), 80);
  }

  const handleNewChat = () => {
    setMessages([]);
    setTrace([]);
  };

  return (
    <div className="dai-app">
      {/* ── LEFT PANEL (75%) ── */}
      <div style={styles.leftPanel}>
        {/* Header */}
        <header style={styles.header}>
          <div style={styles.headerLeft}>
            <button
              onClick={onBack}
              style={styles.backBtn}
              title="Back to home"
            >
              <ArrowLeft size={15} />
            </button>
            <div style={styles.logoMark}>
              <Zap size={16} color="#00D4FF" fill="#00D4FF" />
            </div>
            <span style={styles.logoText}>DAI</span>
            <span style={styles.logoSub}>Dhaya AI</span>
          </div>
          <div style={styles.headerRight}>
            <button
              onClick={handleNewChat}
              style={styles.newChatBtn}
              title="New Chat"
            >
              <SquarePen size={16} />
            </button>
            <div style={styles.statusGroup}>
              <span style={styles.statusDot} />
              <span style={styles.statusText}>Online</span>
            </div>
          </div>
        </header>

        {/* Chat area */}
        <ChatWindow messages={messages} loading={loading} />

        {/* Input */}
        <ChatInput onSend={handleSend} loading={loading} />
      </div>

      {/* ── RIGHT PANEL (25%) ── */}
      <TracePanel trace={trace} />
    </div>
  );
}

function App() {
  const [page, setPage] = useState("landing"); // "landing" | "chat"
  const [heroQuery, setHeroQuery] = useState("");

  const navigateToChat = (query) => {
    setHeroQuery(query);
    setPage("chat");
  };

  const navigateToLanding = () => {
    setHeroQuery("");
    setPage("landing");
  };

  if (page === "chat") {
    return <ChatPage initialQuery={heroQuery} onBack={navigateToLanding} />;
  }

  return <LandingPage onNavigateToChat={navigateToChat} />;
}

const styles = {
  leftPanel: {
    display: "flex",
    flexDirection: "column",
    width: "75%",
    height: "100vh",
    background: "var(--bg-primary)",
    position: "relative",
  },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 28px",
    height: "58px",
    borderBottom: "1px solid var(--border)",
    background: "var(--bg-secondary)",
    flexShrink: 0,
  },
  headerLeft: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
  },
  backBtn: {
    background: "none",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    color: "var(--text-secondary)",
    cursor: "pointer",
    padding: "5px 8px",
    display: "flex",
    alignItems: "center",
    transition: "border-color 0.2s, color 0.2s",
  },
  logoMark: {
    width: "28px",
    height: "28px",
    borderRadius: "7px",
    background: "var(--accent-muted)",
    border: "1px solid rgba(0,212,255,0.3)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  logoText: {
    fontFamily: "var(--font-display)",
    fontWeight: 700,
    fontSize: "18px",
    color: "var(--text-primary)",
    letterSpacing: "0.08em",
  },
  logoSub: {
    fontFamily: "var(--font-body)",
    fontSize: "12px",
    color: "var(--text-muted)",
    paddingLeft: "2px",
    letterSpacing: "0.04em",
  },
  headerRight: {
    display: "flex",
    alignItems: "center",
    gap: "14px",
  },
  newChatBtn: {
    background: "none",
    border: "1px solid var(--border)",
    borderRadius: "8px",
    color: "var(--text-secondary)",
    cursor: "pointer",
    padding: "5px 8px",
    display: "flex",
    alignItems: "center",
    transition: "border-color 0.2s, color 0.2s",
  },
  statusGroup: {
    display: "flex",
    alignItems: "center",
    gap: "6px",
  },
  statusDot: {
    width: "7px",
    height: "7px",
    borderRadius: "50%",
    background: "var(--success)",
    animation: "livePulse 2s infinite",
  },
  statusText: {
    fontSize: "12px",
    color: "var(--text-secondary)",
    fontFamily: "var(--font-mono)",
  },
};

export default App;
